#!/usr/bin/env python3
import argparse
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path


DEFAULT_CONTAINER = "mermaid-cli-local"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True)


def emit(proc: subprocess.CompletedProcess[str]) -> None:
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")


def quote_cmd(cmd: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in cmd)


def fail(msg: str, code: int = 2, hint: str | None = None) -> int:
    print(f"Error: {msg}", file=sys.stderr)
    if hint:
        print(f"Hint: {hint}", file=sys.stderr)
    return code


def docker_inspect_mounts(docker_bin: str, container: str) -> list[dict]:
    proc = run([docker_bin, "inspect", container, "--format", "{{json .Mounts}}"])
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "failed to inspect container").strip()
        raise RuntimeError(detail)
    try:
        return json.loads(proc.stdout.strip() or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"could not parse docker inspect mounts: {exc}") from exc


def container_running(docker_bin: str, container: str) -> bool:
    proc = run([docker_bin, "inspect", "-f", "{{.State.Running}}", container])
    return proc.returncode == 0 and (proc.stdout or "").strip() == "true"


def to_container_path_from_mounts(host_file: Path, mounts: list[dict]) -> str | None:
    host_file = host_file.resolve()
    best: tuple[int, str] | None = None

    for mount in mounts:
        source = mount.get("Source")
        dest = mount.get("Destination")
        if not source or not dest:
            continue

        source_path = Path(source).resolve()
        try:
            rel = host_file.relative_to(source_path)
        except ValueError:
            continue

        candidate = f"{dest.rstrip('/')}/{str(rel).lstrip('/')}" if str(rel) != "." else dest
        score = len(str(source_path))
        if best is None or score > best[0]:
            best = (score, candidate)

    return best[1] if best else None


def map_required_path(path: Path, mounts: list[dict], label: str) -> str:
    mapped = to_container_path_from_mounts(path, mounts)
    if not mapped:
        raise ValueError(
            f"could not map {label} file into container mounts: {path}. "
            f"Place it under a mounted directory or adjust container volumes."
        )
    return mapped


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Mermaid diagrams using mermaid-cli in a running container")
    ap.add_argument("input_file", help="Path to Mermaid .mmd/.mermaid/.md file on host")
    ap.add_argument("--container", default=DEFAULT_CONTAINER, help=f"Running container name (default: {DEFAULT_CONTAINER})")
    ap.add_argument("--docker-bin", default="docker", help="Docker binary to use (default: docker)")
    ap.add_argument("--container-path", help="Explicit input path inside container (skip mount auto-detection for input)")
    ap.add_argument("--output", help="Host output path. Default: input file with selected --format extension")
    ap.add_argument("--format", choices=["svg", "png", "pdf"], default="svg", help="Output format (default: svg)")
    ap.add_argument("--theme", help="Mermaid theme (e.g. default, neutral, dark, forest)")
    ap.add_argument("--background", help="Background color (e.g. transparent)")
    ap.add_argument("--config", help="Path to Mermaid config JSON file on host")
    ap.add_argument("--css", help="Path to CSS file to inline")
    ap.add_argument("--check-only", action="store_true", help="Validate by rendering to a temp container path; do not produce host output")
    ap.add_argument("--verbose", action="store_true", help="Print command being executed")
    args = ap.parse_args()

    input_path = Path(args.input_file).expanduser().resolve()
    if not input_path.exists() or not input_path.is_file():
        return fail(f"input file not found: {input_path}")

    config_path = Path(args.config).expanduser().resolve() if args.config else None
    css_path = Path(args.css).expanduser().resolve() if args.css else None

    for p, label in [(config_path, "--config"), (css_path, "--css")]:
        if p and (not p.exists() or not p.is_file()):
            return fail(f"{label} file not found: {p}")

    try:
        mounts = docker_inspect_mounts(args.docker_bin, args.container)
    except RuntimeError as exc:
        detail = str(exc).lower()
        hint = "Start the container first, or pass --container <running-name> for your environment."
        if "permission denied" in detail:
            hint = "Docker daemon access is required. Add your user to the docker group or run with sudo."
        elif "cannot connect" in detail or "is the docker daemon running" in detail:
            hint = "Start Docker daemon/service, then rerun."
        return fail(str(exc), hint=hint)

    if not container_running(args.docker_bin, args.container):
        return fail(
            f"container '{args.container}' is not running",
            hint=f"Start it first: {args.docker_bin} start {args.container}",
        )

    try:
        if args.container_path:
            container_input = args.container_path
        else:
            container_input = map_required_path(input_path, mounts, "input")

        if args.check_only:
            container_output = f"/tmp/mermaid-validate-{int(time.time() * 1000)}.{args.format}"
            host_output = None
        else:
            if args.output:
                host_output = Path(args.output).expanduser().resolve()
            else:
                host_output = input_path.with_suffix(f".{args.format}")

            host_output.parent.mkdir(parents=True, exist_ok=True)
            container_output = map_required_path(host_output, mounts, "output")

        container_config = map_required_path(config_path, mounts, "config") if config_path else None
        container_css = map_required_path(css_path, mounts, "css") if css_path else None
    except ValueError as exc:
        return fail(str(exc))

    cmd = [
        args.docker_bin,
        "exec",
        args.container,
        "/home/mermaidcli/node_modules/.bin/mmdc",
        "-i",
        container_input,
        "-o",
        container_output,
    ]

    if args.theme:
        cmd.extend(["-t", args.theme])
    if args.background:
        cmd.extend(["-b", args.background])
    if container_config:
        cmd.extend(["-c", container_config])
    if container_css:
        cmd.extend(["--cssFile", container_css])

    if args.verbose:
        print("Running:")
        print(quote_cmd(cmd))

    proc = run(cmd)
    emit(proc)

    if proc.returncode == 0:
        if args.check_only:
            print("PASS: render succeeded (check-only)")
        else:
            print(f"PASS: render succeeded -> {host_output}")
        return 0

    combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).lower()
    if "permission denied" in combined and "docker" in combined:
        return fail(
            "Docker daemon access denied",
            hint="Add your user to the docker group or run with sudo.",
        )
    if "no such container" in combined or "is not running" in combined:
        return fail(
            f"container '{args.container}' is unavailable",
            hint=f"Start it first: {args.docker_bin} start {args.container}",
        )

    print("FAIL: Mermaid render/validation error", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
