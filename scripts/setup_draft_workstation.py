#!/usr/bin/env python3
"""Bootstrap local draft-render dependencies for this draft repo."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
WSL_DRAFT_PACKAGES = (
    "git",
    "make",
    "python3-pip",
    "python3-venv",
    "ruby-bundler",
    "npm",
    "libxml2-utils",
    "curl",
    "jq",
)
WINDOWS_DRIVE_RE = re.compile(r"^([A-Za-z]):[\\/](.*)$")


class SetupError(RuntimeError):
    """Raised when draft workstation bootstrap fails."""


def run_process(args: list[str], *, cwd: Path | None = None, capture: bool = False, env: dict[str, str] | None = None) -> str:
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        env={**os.environ, **(env or {})},
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        check=False,
    )
    output = completed.stdout or ""
    if completed.returncode != 0:
        detail = f"\n{output.strip()}" if output.strip() else ""
        raise SetupError(f"command failed with exit code {completed.returncode}: {' '.join(args)}{detail}")
    return output


def native_environment_available() -> bool:
    required = ("git", "make", "python3", "ruby")
    return all(shutil.which(command_name) is not None for command_name in required)


def ensure_native_prerequisites() -> dict[str, str]:
    environment: dict[str, str] = {}
    missing = [
        command_name
        for command_name in ("git", "make", "python3", "ruby")
        if shutil.which(command_name) is None
    ]
    if missing:
        raise SetupError(
            "native draft rendering requires these commands on PATH: "
            + ", ".join(missing)
        )

    if shutil.which("bundle") is not None:
        return environment
    if shutil.which("gem") is None:
        raise SetupError("bundle is not on PATH and gem is unavailable for a local Bundler install")

    run_process(["gem", "install", "--user-install", "bundler"])
    gem_user_dir = run_process(["ruby", "-e", "print Gem.user_dir"], capture=True).strip()
    gem_bin = Path(gem_user_dir) / "bin"
    environment["PATH"] = str(gem_bin) + os.pathsep + os.environ.get("PATH", "")
    if shutil.which("bundle", path=environment["PATH"]) is None:
        raise SetupError("bundler installed, but the bundle executable is still not available on PATH")
    return environment


def wsl_executable() -> str:
    candidate = shutil.which("wsl.exe") or shutil.which("wsl")
    if candidate is None:
        raise SetupError("WSL is not available on PATH")
    return candidate


def list_wsl_distros() -> list[str]:
    output = run_process([wsl_executable(), "-l", "-q"], capture=True)
    return [line.strip().strip("\x00") for line in output.splitlines() if line.strip().strip("\x00")]


def choose_wsl_distro(requested: str | None) -> str:
    distros = list_wsl_distros()
    if not distros:
        raise SetupError("no WSL distributions are installed")
    if requested:
        if requested in distros:
            return requested
        raise SetupError(
            f"requested WSL distro {requested!r} is not installed. Available distros: {', '.join(distros)}"
        )
    for distro in distros:
        if "ubuntu" in distro.lower():
            return distro
    return distros[0]


def windows_path_to_wsl_path(path: Path | str) -> str:
    text = str(path)
    match = WINDOWS_DRIVE_RE.match(text)
    if match is None:
        raise SetupError(f"could not translate a Windows path into WSL form: {text}")
    drive, rest = match.groups()
    return f"/mnt/{drive.lower()}/{rest.replace(chr(92), '/')}"


def run_wsl_bash(distro: str, script: str) -> None:
    run_process([wsl_executable(), "-d", distro, "--", "bash", "-lc", script])


def install_wsl_dependencies(distro: str) -> None:
    package_list = " ".join(WSL_DRAFT_PACKAGES)
    run_wsl_bash(distro, f"sudo apt-get update && sudo apt-get install -y {package_list}")


def draft_outputs_present() -> bool:
    return (REPO_ROOT / f"{REPO_ROOT.name}.html").exists() and (REPO_ROOT / f"{REPO_ROOT.name}.txt").exists()


def command_bootstrap(args: argparse.Namespace) -> int:
    if platform.system() == "Windows":
        if native_environment_available():
            environment = ensure_native_prerequisites()
            run_process(["make", "PRE_SETUP=true", "latest"], cwd=REPO_ROOT, env=environment)
            return 0
        if not args.use_wsl:
            raise SetupError(
                "native Windows draft prerequisites were not found on PATH. "
                "Install git/make/python3/ruby for native rendering, or rerun with --use-wsl."
            )
        distro = choose_wsl_distro(args.wsl_distro)
        if args.install_wsl_deps:
            install_wsl_dependencies(distro)
        repo_wsl_path = windows_path_to_wsl_path(REPO_ROOT.resolve())
        run_wsl_bash(distro, f"cd {shlex.quote(repo_wsl_path)} && make PRE_SETUP=true latest")
        return 0

    environment = ensure_native_prerequisites()
    run_process(["make", "PRE_SETUP=true", "latest"], cwd=REPO_ROOT, env=environment)
    return 0


def command_status(_: argparse.Namespace) -> int:
    print(f"Draft repo: {REPO_ROOT}")
    print(f"Render outputs: {'present' if draft_outputs_present() else 'missing'}")
    print(f"Template checkout: {'present' if (REPO_ROOT / 'lib').exists() else 'missing'}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap local draft-render dependencies for this draft repo.")
    subparsers = parser.add_subparsers(dest="command")

    bootstrap = subparsers.add_parser(
        "bootstrap",
        help="Bootstrap the local i-d-template checkout and render this draft repo.",
    )
    bootstrap.add_argument(
        "--use-wsl",
        action="store_true",
        help="On Windows, use WSL as an explicit fallback when native POSIX tooling is unavailable.",
    )
    bootstrap.add_argument(
        "--install-wsl-deps",
        action="store_true",
        help="On Windows, after --use-wsl, install the draft-render prerequisites inside the chosen WSL distro.",
    )
    bootstrap.add_argument(
        "--wsl-distro",
        help="On Windows, explicit WSL distro name to use for draft rendering.",
    )
    bootstrap.set_defaults(func=command_bootstrap)

    status = subparsers.add_parser(
        "status",
        help="Report whether this draft repo has local render outputs and a template checkout.",
    )
    status.set_defaults(func=command_status)

    args = parser.parse_args(argv)
    if args.command is None:
        args.command = "bootstrap"
        args.func = command_bootstrap
        args.use_wsl = False
        args.install_wsl_deps = False
        args.wsl_distro = None
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        return args.func(args)
    except (OSError, SetupError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
