#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True)


def emit(proc: subprocess.CompletedProcess[str]) -> None:
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, file=sys.stderr, end="")


def docker_inspect_mounts(docker_bin: str, container: str) -> list[dict]:
    proc = run([docker_bin, "inspect", container, "--format", "{{json .Mounts}}"])
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "failed to inspect container").strip())
    try:
        return json.loads(proc.stdout.strip() or "[]")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"could not parse docker inspect mounts: {exc}") from exc


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


def build_container_exec_cmd(docker_bin: str, container: str, container_file: str) -> list[str]:
    # Use the same official parser shipped in structurizr/structurizr image.
    return [
        docker_bin,
        "exec",
        container,
        "java",
        "-jar",
        "/usr/local/structurizr.war",
        "validate",
        "-workspace",
        container_file,
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Structurizr DSL using a running Structurizr container")
    ap.add_argument("dsl_file", help="Path to .dsl file on host")
    ap.add_argument("--container", default="structurizr-local", help="Running container name (default: structurizr-local)")
    ap.add_argument("--container-path", help="Explicit .dsl path inside container (skip mount auto-detection)")
    ap.add_argument("--docker-bin", default="docker", help="Docker binary to use (default: docker)")
    ap.add_argument("--verbose", action="store_true", help="Print command being executed")
    args = ap.parse_args()

    dsl_path = Path(args.dsl_file).expanduser().resolve()
    if not dsl_path.exists():
        print(f"Error: file not found: {dsl_path}", file=sys.stderr)
        return 2

    container_file = args.container_path
    if not container_file:
        try:
            mounts = docker_inspect_mounts(args.docker_bin, args.container)
        except RuntimeError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            print(
                f"Hint: start the container first, or pass --container <name> for your setup.",
                file=sys.stderr,
            )
            return 2

        container_file = to_container_path_from_mounts(dsl_path, mounts)
        if not container_file:
            print(
                "Error: could not map host file into container mounts. "
                "Pass --container-path <path-inside-container>.",
                file=sys.stderr,
            )
            return 2

    cmd = build_container_exec_cmd(args.docker_bin, args.container, container_file)

    if args.verbose:
        print("Running:")
        print(" ".join(cmd))

    proc = run(cmd)
    emit(proc)

    if proc.returncode != 0:
        combined = ((proc.stdout or "") + "\n" + (proc.stderr or "")).lower()
        if "permission denied" in combined and "docker" in combined:
            print(
                "\nHint: Docker daemon access is required. Try running with sudo or add your user to the docker group.",
                file=sys.stderr,
            )
        if "is not running" in combined or "no such container" in combined:
            print(
                f"\nHint: start the container first (or pass --container <running-name>).",
                file=sys.stderr,
            )

    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
