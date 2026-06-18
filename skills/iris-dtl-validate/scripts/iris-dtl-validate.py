#!/usr/bin/env python3
import argparse
import difflib
import re
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path


DEFAULT_CONTAINER = "iris-dtl-validate"


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, input=input_text)


def emit(proc: subprocess.CompletedProcess[str]) -> None:
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")


def quote_cmd(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def fail(msg: str, *, code: int = 3, hint: str | None = None) -> int:
    print(f"Error: {msg}", file=sys.stderr)
    if hint:
        print(f"Hint: {hint}", file=sys.stderr)
    return code


def normalize_hl7_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.rstrip("\n")


def parse_attr(tag_text: str, name: str) -> str | None:
    m = re.search(rf"\b{name}\s*=\s*(['\"])(.*?)\1", tag_text, flags=re.IGNORECASE | re.DOTALL)
    return m.group(2).strip() if m else None


def parse_dtl_metadata(dtl_path: Path) -> tuple[str, str, str]:
    text = dtl_path.read_text(encoding="utf-8", errors="replace")

    class_match = re.search(
        r"(?im)^\s*Class\s+([A-Za-z%][A-Za-z0-9_\.%]*)\s+Extends\s+Ens\.DataTransformDTL\b",
        text,
    )
    if not class_match:
        raise ValueError("Could not find 'Class <name> Extends Ens.DataTransformDTL' in the .cls file")
    class_name = class_match.group(1)

    transform_match = re.search(r"<transform\b[^>]*>", text, flags=re.IGNORECASE | re.DOTALL)
    if not transform_match:
        raise ValueError("Could not find <transform ...> element in the DTL XData block")

    transform_tag = transform_match.group(0)
    source_class = parse_attr(transform_tag, "sourceClass") or ""
    source_doc_type = parse_attr(transform_tag, "sourceDocType") or ""

    if not source_class:
        raise ValueError("DTL <transform> is missing sourceClass attribute")

    return class_name, source_class, source_doc_type


def docker_check_access(docker_bin: str) -> tuple[bool, str]:
    proc = run([docker_bin, "info"])
    if proc.returncode == 0:
        return True, ""
    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return False, combined


def container_exists(docker_bin: str, container: str) -> bool:
    return run([docker_bin, "container", "inspect", container]).returncode == 0


def container_running(docker_bin: str, container: str) -> bool:
    proc = run([docker_bin, "inspect", "-f", "{{.State.Running}}", container])
    return proc.returncode == 0 and (proc.stdout or "").strip() == "true"


def ensure_running_container(docker_bin: str, container: str) -> int:
    if not container_exists(docker_bin, container):
        return fail(
            f"Container '{container}' does not exist",
            code=3,
            hint="Create/start it first, or pass --container <running-name> for your environment."
        )

    if not container_running(docker_bin, container):
        return fail(
            f"Container '{container}' is not running",
            code=3,
            hint=f"Start it first: {docker_bin} start {container}",
        )

    return 0


def docker_cp_to_container(
    docker_bin: str,
    container: str,
    host_path: Path,
    container_path: str,
    *,
    verbose: bool,
) -> int:
    cmd = [docker_bin, "cp", str(host_path), f"{container}:{container_path}"]
    if verbose:
        print("Running:")
        print(quote_cmd(cmd))
    proc = run(cmd)
    emit(proc)
    if proc.returncode != 0:
        return fail(f"Failed to copy {host_path} to {container}:{container_path}")
    return 0


def clean_session_output(text: str) -> str:
    lines = text.replace("\r", "").splitlines()
    cleaned: list[str] = []
    for line in lines:
        if line.startswith("USER>"):
            continue
        if line.startswith("Node:"):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def run_iris_session(
    docker_bin: str,
    container: str,
    objectscript: str,
    *,
    verbose: bool,
) -> subprocess.CompletedProcess[str]:
    cmd = [docker_bin, "exec", "-i", container, "iris", "session", "IRIS", "-U", "USER"]
    if verbose:
        print("Running:")
        print(quote_cmd(cmd))
        print("-- ObjectScript --")
        print(objectscript)
        print("------------------")
    return run(cmd, input_text=objectscript)


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate an IRIS DTL against HL7 input/expected fixtures")
    ap.add_argument("--dtl", required=True, help="Path to DTL .cls file")
    ap.add_argument("--input", required=True, help="Path to HL7 input message file")
    ap.add_argument("--expected", required=True, help="Path to HL7 expected output message file")
    ap.add_argument("--container", default=DEFAULT_CONTAINER, help=f"Running container name (default: {DEFAULT_CONTAINER})")
    ap.add_argument("--docker-bin", default="docker", help="Docker binary to use (default: docker)")
    ap.add_argument("--keep-output", help="Write normalized actual output to this host path")
    ap.add_argument("--verbose", action="store_true", help="Print commands being executed")
    args = ap.parse_args()

    dtl_path = Path(args.dtl).expanduser().resolve()
    in_path = Path(args.input).expanduser().resolve()
    expected_path = Path(args.expected).expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]

    for p, label in [(dtl_path, "--dtl"), (in_path, "--input"), (expected_path, "--expected")]:
        if not p.exists():
            return fail(f"{label} path not found: {p}", code=2)
        if p.is_dir():
            return fail(f"{label} must be a file, not a directory: {p}", code=2)

    if dtl_path.suffix.lower() != ".cls":
        return fail("--dtl must point to a single .cls file", code=2)

    try:
        dtl_class, source_class, source_doc_type = parse_dtl_metadata(dtl_path)
    except ValueError as ex:
        return fail(str(ex), code=2)

    if source_class != "EnsLib.HL7.Message":
        return fail(f"v1 supports HL7v2 only (found sourceClass={source_class})", code=2)

    ok, details = docker_check_access(args.docker_bin)
    if not ok:
        lower = details.lower()
        hint = None
        if "permission denied" in lower:
            hint = "Docker daemon access is required. Add your user to the docker group or run with sudo."
        elif "cannot connect" in lower or "is the docker daemon running" in lower:
            hint = "Start Docker daemon/service, then rerun."
        return fail("Docker is not available", hint=hint)

    container_rc = ensure_running_container(args.docker_bin, args.container)
    if container_rc != 0:
        return container_rc

    stamp = int(time.time() * 1000)
    runner_host = skill_root / "runner" / "Test.Runner.cls"
    runner_in_container = f"/tmp/Test.Runner-{stamp}.cls"
    dtl_in_container = f"/tmp/DTL-{stamp}.cls"
    in_in_container = f"/tmp/input-{stamp}.txt"
    out_in_container = f"/tmp/output-{stamp}.txt"

    for host, target in [
        (runner_host, runner_in_container),
        (dtl_path, dtl_in_container),
        (in_path, in_in_container),
    ]:
        rc = docker_cp_to_container(args.docker_bin, args.container, host, target, verbose=args.verbose)
        if rc != 0:
            return rc

    objectscript = "\n".join(
        [
            f'set sc=$system.OBJ.Load("{runner_in_container}","ck-d")',
            "if sc '= 1 write \"RESULT=ERROR\",!,\"  \",$system.Status.GetErrorText(sc),!",
            "if sc '= 1 halt",
            f'set sc=$system.OBJ.Load("{dtl_in_container}","ck-d")',
            "if sc '= 1 write \"RESULT=ERROR\",!,\"  \",$system.Status.GetErrorText(sc),!",
            "if sc '= 1 halt",
            f'set sc=##class(Test.Runner).Run("{dtl_class}","{source_doc_type}","{in_in_container}","{out_in_container}")',
            "if sc '= 1 halt",
            "halt",
            "",
        ]
    )

    run_proc = run_iris_session(args.docker_bin, args.container, objectscript, verbose=args.verbose)
    session_out = clean_session_output((run_proc.stdout or "") + ("\n" + run_proc.stderr if run_proc.stderr else ""))
    if session_out:
        print(session_out)

    if run_proc.returncode == 2 or "RESULT=ERROR" in session_out:
        return 2
    if run_proc.returncode != 0:
        return fail(
            "Failed to execute IRIS session command",
            hint=f"Inspect container logs: {args.docker_bin} logs {args.container}",
        )

    with tempfile.TemporaryDirectory(prefix="iris-dtl-validate-") as tmpdir:
        host_raw_output = Path(tmpdir) / "output.txt"
        cp_cmd = [args.docker_bin, "cp", f"{args.container}:{out_in_container}", str(host_raw_output)]
        if args.verbose:
            print("Running:")
            print(quote_cmd(cp_cmd))
        cp_proc = run(cp_cmd)
        emit(cp_proc)
        if cp_proc.returncode != 0:
            return fail(
                f"Failed to copy output file from container path {out_in_container}",
                hint="Check whether the transform produced an output message.",
            )

        actual_text = normalize_hl7_text(host_raw_output.read_text(encoding="utf-8", errors="replace"))

    expected_text = normalize_hl7_text(expected_path.read_text(encoding="utf-8", errors="replace"))

    if args.keep_output:
        keep_path = Path(args.keep_output).expanduser().resolve()
        keep_path.parent.mkdir(parents=True, exist_ok=True)
        keep_path.write_text(actual_text, encoding="utf-8")

    if expected_text == actual_text:
        print("PASS: output matches expected")
        return 0

    diff = difflib.unified_diff(
        expected_text.split("\n"),
        actual_text.split("\n"),
        fromfile=str(expected_path),
        tofile="actual",
        lineterm="",
    )
    for line in diff:
        print(line)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
