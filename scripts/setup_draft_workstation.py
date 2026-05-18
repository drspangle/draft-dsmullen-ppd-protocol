#!/usr/bin/env python3
"""Bootstrap local draft-render dependencies for this draft repo."""

from __future__ import annotations

import argparse
import inspect
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLING_ROOT = REPO_ROOT / ".tooling"
LOCAL_NODE_ROOT = TOOLING_ROOT / "node" / "current"
POSIX_ENV_SCRIPT = TOOLING_ROOT / "env.sh"
POWERSHELL_ENV_SCRIPT = TOOLING_ROOT / "env.ps1"
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
NODE_VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+$")


class SetupError(RuntimeError):
    """Raised when draft workstation bootstrap fails."""


def run_process(
    args: list[str],
    *,
    cwd: Path | None = None,
    capture: bool = False,
    env: dict[str, str] | None = None,
) -> str:
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


def effective_path(environment: dict[str, str] | None = None) -> str:
    if environment and "PATH" in environment:
        return environment["PATH"]
    return os.environ.get("PATH", "")


def resolve_command(command_name: str, environment: dict[str, str] | None = None) -> str | None:
    return shutil.which(command_name, path=effective_path(environment))


def prepend_path(environment: dict[str, str], entry: Path) -> None:
    current_path = effective_path(environment)
    environment["PATH"] = str(entry) + (os.pathsep + current_path if current_path else "")


def local_node_bin_dir() -> Path | None:
    candidate = LOCAL_NODE_ROOT if platform.system() == "Windows" else LOCAL_NODE_ROOT / "bin"
    return candidate if candidate.exists() else None


def add_repo_local_node_to_environment(environment: dict[str, str]) -> None:
    candidate = local_node_bin_dir()
    if candidate is not None:
        prepend_path(environment, candidate)


def missing_commands(
    command_names: tuple[str, ...],
    environment: dict[str, str] | None = None,
) -> list[str]:
    return [command_name for command_name in command_names if resolve_command(command_name, environment) is None]


def native_environment_available() -> bool:
    return not missing_commands(("git", "make", "python3", "ruby"))


def node_platform_descriptor() -> tuple[str, str]:
    system_name = platform.system()
    machine_name = platform.machine().lower()
    if machine_name in {"x86_64", "amd64", "x64"}:
        architecture = "x64"
    elif machine_name in {"arm64", "aarch64"}:
        architecture = "arm64"
    else:
        raise SetupError(f"unsupported CPU architecture for repo-local Node.js bootstrap: {platform.machine()}")

    if system_name == "Darwin":
        return f"darwin-{architecture}", "tar.gz"
    if system_name == "Linux":
        return f"linux-{architecture}", "tar.xz"
    if system_name == "Windows":
        return f"win-{architecture}", "zip"
    raise SetupError(f"unsupported operating system for repo-local Node.js bootstrap: {system_name}")


def fetch_json(url: str) -> object:
    try:
        with urlopen(url) as response:
            return json.load(response)
    except HTTPError as exc:
        raise SetupError(f"failed to fetch {url}: HTTP {exc.code}") from exc
    except URLError as exc:
        raise SetupError(f"failed to fetch {url}: {exc.reason}") from exc


def resolve_node_version(version_spec: str) -> str:
    if version_spec == "lts":
        releases = fetch_json("https://nodejs.org/dist/index.json")
        if not isinstance(releases, list):
            raise SetupError("unexpected Node.js release index format")
        for release in releases:
            if isinstance(release, dict) and release.get("lts") and isinstance(release.get("version"), str):
                return release["version"]
        raise SetupError("could not find an LTS Node.js release in the Node.js distribution index")
    if NODE_VERSION_RE.fullmatch(version_spec):
        return version_spec if version_spec.startswith("v") else f"v{version_spec}"
    raise SetupError("node version must be 'lts' or an exact version like 'v22.15.0'")


def download_file(url: str, destination: Path) -> None:
    try:
        with urlopen(url) as response, destination.open("wb") as output_file:
            shutil.copyfileobj(response, output_file)
    except HTTPError as exc:
        raise SetupError(f"failed to download {url}: HTTP {exc.code}") from exc
    except URLError as exc:
        raise SetupError(f"failed to download {url}: {exc.reason}") from exc


def is_within_directory(directory: Path, target: Path) -> bool:
    try:
        target.relative_to(directory)
    except ValueError:
        return False
    return True


def safe_extract_tar(archive_path: Path, destination: Path) -> None:
    with tarfile.open(archive_path, "r:*") as archive:
        for member in archive.getmembers():
            member_path = destination / member.name
            if not is_within_directory(destination.resolve(), member_path.resolve()):
                raise SetupError(f"refusing to extract unsafe archive member: {member.name}")
        extract_kwargs: dict[str, str] = {}
        if "filter" in inspect.signature(archive.extractall).parameters:
            extract_kwargs["filter"] = "data"
        archive.extractall(destination, **extract_kwargs)


def safe_extract_zip(archive_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        for member_name in archive.namelist():
            member_path = destination / member_name
            if not is_within_directory(destination.resolve(), member_path.resolve()):
                raise SetupError(f"refusing to extract unsafe archive member: {member_name}")
        archive.extractall(destination)


def write_tooling_environment_scripts() -> None:
    TOOLING_ROOT.mkdir(parents=True, exist_ok=True)
    POSIX_ENV_SCRIPT.write_text(
        "#!/bin/sh\n"
        'REPO_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"\n'
        'export PATH="$REPO_ROOT/.tooling/node/current/bin:$PATH"\n',
        encoding="utf-8",
    )
    POSIX_ENV_SCRIPT.chmod(0o755)
    POWERSHELL_ENV_SCRIPT.write_text(
        "$repoRoot = Split-Path -Parent $PSScriptRoot\n"
        '$env:PATH = "$repoRoot\\.tooling\\node\\current;$env:PATH"\n',
        encoding="utf-8",
    )


def install_repo_local_node(node_version_spec: str) -> str:
    node_version = resolve_node_version(node_version_spec)
    platform_name, archive_extension = node_platform_descriptor()
    archive_name = f"node-{node_version}-{platform_name}.{archive_extension}"
    archive_url = f"https://nodejs.org/dist/{node_version}/{archive_name}"
    TOOLING_ROOT.mkdir(parents=True, exist_ok=True)
    local_node_parent = LOCAL_NODE_ROOT.parent
    local_node_parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="node-bootstrap-", dir=str(TOOLING_ROOT)) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        archive_path = temp_dir / archive_name
        extract_path = temp_dir / "extract"
        staging_path = local_node_parent / ".staging"
        extract_path.mkdir()
        download_file(archive_url, archive_path)
        if archive_extension == "zip":
            safe_extract_zip(archive_path, extract_path)
        else:
            safe_extract_tar(archive_path, extract_path)
        extracted_roots = [path for path in extract_path.iterdir() if path.is_dir()]
        if len(extracted_roots) != 1:
            raise SetupError(f"unexpected Node.js archive contents in {archive_name}")
        if staging_path.exists():
            shutil.rmtree(staging_path)
        shutil.move(str(extracted_roots[0]), str(staging_path))
        if LOCAL_NODE_ROOT.exists():
            shutil.rmtree(LOCAL_NODE_ROOT)
        staging_path.rename(LOCAL_NODE_ROOT)

    write_tooling_environment_scripts()
    return node_version


def ensure_submission_prerequisites(
    environment: dict[str, str],
    *,
    install_submission_tools: bool,
    node_version: str,
) -> None:
    if resolve_command("xmllint", environment) is None:
        raise SetupError("submission validation requires xmllint on PATH")
    if resolve_command("npm", environment) is None:
        if not install_submission_tools:
            raise SetupError(
                "submission validation requires npm on PATH or a repo-local Node.js toolchain. "
                "Re-run bootstrap with --submission-tools."
            )
        install_repo_local_node(node_version)
        add_repo_local_node_to_environment(environment)
    if resolve_command("npm", environment) is None:
        raise SetupError("npm is still unavailable after repo-local Node.js bootstrap")


def ensure_native_prerequisites(
    *,
    require_submission_tools: bool = False,
    install_submission_tools: bool = False,
    node_version: str = "lts",
) -> dict[str, str]:
    environment: dict[str, str] = {}
    add_repo_local_node_to_environment(environment)
    missing = missing_commands(("git", "make", "python3", "ruby"), environment)
    if missing:
        raise SetupError(
            "native draft rendering requires these commands on PATH: "
            + ", ".join(missing)
        )

    if resolve_command("bundle", environment) is None:
        if resolve_command("gem", environment) is None:
            raise SetupError("bundle is not on PATH and gem is unavailable for a local Bundler install")
        run_process(["gem", "install", "--user-install", "bundler"])
        gem_user_dir = run_process(["ruby", "-e", "print Gem.user_dir"], capture=True).strip()
        gem_bin = Path(gem_user_dir) / "bin"
        prepend_path(environment, gem_bin)
        if resolve_command("bundle", environment) is None:
            raise SetupError("bundler installed, but the bundle executable is still not available on PATH")

    if require_submission_tools or install_submission_tools:
        ensure_submission_prerequisites(
            environment,
            install_submission_tools=install_submission_tools,
            node_version=node_version,
        )
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


def run_make_targets(environment: dict[str, str], *targets: str) -> None:
    run_process(["make", *targets], cwd=REPO_ROOT, env=environment)


def local_idnits_executable() -> Path:
    executable_name = "idnits.cmd" if platform.system() == "Windows" else "idnits"
    return REPO_ROOT / "node_modules" / ".bin" / executable_name


def ensure_local_idnits(environment: dict[str, str]) -> Path:
    executable_path = local_idnits_executable()
    if not executable_path.exists():
        run_process(
            ["npm", "install", "-q", "--no-save", "github:ietf-tools/idnits"],
            cwd=REPO_ROOT,
            env=environment,
        )
    if not executable_path.exists():
        raise SetupError("idnits installation completed, but the executable is still missing")
    return executable_path


def latest_versioned_xml_path() -> Path:
    candidates = sorted((REPO_ROOT / "versioned").glob(f"{REPO_ROOT.name}-*.xml"))
    if not candidates:
        raise SetupError("no versioned XML output was found after make next")
    return candidates[-1]


def parse_idnits_report(output: str) -> dict[str, object]:
    json_start = output.find("{")
    if json_start == -1:
        raise SetupError("idnits did not produce JSON output")
    try:
        parsed = json.loads(output[json_start:])
    except json.JSONDecodeError as exc:
        raise SetupError("idnits JSON output could not be parsed") from exc
    if not isinstance(parsed, dict):
        raise SetupError("unexpected idnits JSON output shape")
    return parsed


def enforce_idnits_result(environment: dict[str, str], *, mode: str = "submission") -> None:
    idnits_executable = ensure_local_idnits(environment)
    xml_path = latest_versioned_xml_path()
    report_output = run_process(
        [str(idnits_executable), "-o", "json", "-m", mode, str(xml_path)],
        cwd=REPO_ROOT,
        capture=True,
        env=environment,
    )
    report = parse_idnits_report(report_output)
    severity_counts = report.get("nitsBySeverity")
    if not isinstance(severity_counts, dict):
        raise SetupError("idnits report did not include severity counts")
    error_count = int(severity_counts.get("error", 0))
    warning_count = int(severity_counts.get("warning", 0))
    comment_count = int(severity_counts.get("comment", 0))
    if error_count:
        first_error = ""
        nits = report.get("nits")
        if isinstance(nits, list):
            for nit in nits:
                if isinstance(nit, dict) and nit.get("severity") == "ValidationError":
                    code = nit.get("code", "UNKNOWN")
                    desc = nit.get("desc", "")
                    first_error = f" First error: {code} - {desc}".rstrip()
                    break
        raise SetupError(
            f"idnits reported {error_count} error(s), {warning_count} warning(s), "
            f"and {comment_count} comment(s).{first_error}"
        )
    print(
        f"idnits passed with {warning_count} warning(s) and {comment_count} comment(s) "
        f"for {xml_path.name}."
    )


def wsl_bootstrap_path(args: argparse.Namespace) -> tuple[str, str]:
    if args.submission_tools:
        raise SetupError(
            "repo-local submission tooling bootstrap is only supported in the native environment. "
            "For WSL fallback, use validate-submission --use-wsl --install-wsl-deps."
        )
    distro = choose_wsl_distro(args.wsl_distro)
    if args.install_wsl_deps:
        install_wsl_dependencies(distro)
    return distro, windows_path_to_wsl_path(REPO_ROOT.resolve())


def describe_readiness(missing: list[str]) -> str:
    if not missing:
        return "ready"
    return "missing: " + ", ".join(missing)


def local_node_version(environment: dict[str, str]) -> str | None:
    if local_node_bin_dir() is None or resolve_command("node", environment) is None:
        return None
    try:
        return run_process(["node", "--version"], capture=True, env=environment).strip()
    except SetupError:
        return None


def ensure_native_submission_environment(args: argparse.Namespace) -> dict[str, str]:
    return ensure_native_prerequisites(
        require_submission_tools=True,
        install_submission_tools=args.submission_tools,
        node_version=args.node_version,
    )


def command_bootstrap(args: argparse.Namespace) -> int:
    if platform.system() == "Windows":
        if native_environment_available():
            environment = ensure_native_prerequisites(
                require_submission_tools=args.submission_tools,
                install_submission_tools=args.submission_tools,
                node_version=args.node_version,
            )
            run_make_targets(environment, "PRE_SETUP=true", "latest")
            return 0
        if not args.use_wsl:
            raise SetupError(
                "native Windows draft prerequisites were not found on PATH. "
                "Install git/make/python3/ruby for native rendering, or rerun with --use-wsl."
            )
        distro, repo_wsl_path = wsl_bootstrap_path(args)
        run_wsl_bash(distro, f"cd {shlex.quote(repo_wsl_path)} && make PRE_SETUP=true latest")
        return 0

    environment = ensure_native_prerequisites(
        require_submission_tools=args.submission_tools,
        install_submission_tools=args.submission_tools,
        node_version=args.node_version,
    )
    run_make_targets(environment, "PRE_SETUP=true", "latest")
    return 0


def command_status(_: argparse.Namespace) -> int:
    environment: dict[str, str] = {}
    add_repo_local_node_to_environment(environment)
    render_missing = missing_commands(("git", "make", "python3", "ruby"), environment)
    submission_missing = missing_commands(("xmllint", "npm"), environment)
    print(f"Draft repo: {REPO_ROOT}")
    print(f"Render outputs: {'present' if draft_outputs_present() else 'missing'}")
    print(f"Template checkout: {'present' if (REPO_ROOT / 'lib').exists() else 'missing'}")
    print(f"Render prerequisites: {describe_readiness(render_missing)}")
    print(f"Bundler: {'ready' if resolve_command('bundle', environment) is not None else 'missing'}")
    print(f"Submission prerequisites: {describe_readiness(submission_missing)}")
    node_version = local_node_version(environment)
    if node_version is None:
        print("Repo-local Node.js toolchain: missing")
    else:
        print(f"Repo-local Node.js toolchain: present ({node_version})")
    print(f"POSIX env helper: {'present' if POSIX_ENV_SCRIPT.exists() else 'missing'}")
    print(f"PowerShell env helper: {'present' if POWERSHELL_ENV_SCRIPT.exists() else 'missing'}")
    return 0


def command_validate_submission(args: argparse.Namespace) -> int:
    if platform.system() == "Windows":
        if native_environment_available():
            environment = ensure_native_submission_environment(args)
            run_make_targets(environment, "next")
            enforce_idnits_result(environment)
            return 0
        if not args.use_wsl:
            raise SetupError(
                "native Windows draft prerequisites were not found on PATH. "
                "Install git/make/python3/ruby for native submission checks, or rerun with --use-wsl."
            )
        distro = choose_wsl_distro(args.wsl_distro)
        if args.install_wsl_deps:
            install_wsl_dependencies(distro)
        repo_wsl_path = windows_path_to_wsl_path(REPO_ROOT.resolve())
        run_wsl_bash(
            distro,
            "cd "
            + shlex.quote(repo_wsl_path)
            + " && make next && "
            + "python3 scripts/setup_draft_workstation.py validate-submission",
        )
        return 0

    environment = ensure_native_submission_environment(args)
    run_make_targets(environment, "next")
    enforce_idnits_result(environment)
    return 0


def add_wsl_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--use-wsl",
        action="store_true",
        help="On Windows, use WSL as an explicit fallback when native POSIX tooling is unavailable.",
    )
    parser.add_argument(
        "--install-wsl-deps",
        action="store_true",
        help="On Windows, after --use-wsl, install the draft-render prerequisites inside the chosen WSL distro.",
    )
    parser.add_argument(
        "--wsl-distro",
        help="On Windows, explicit WSL distro name to use for draft rendering.",
    )


def add_submission_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--submission-tools",
        action="store_true",
        help=(
            "Also ensure native pre-submit tooling for idnits. "
            "If npm is missing, install a repo-local Node.js toolchain under .tooling/."
        ),
    )
    parser.add_argument(
        "--node-version",
        default="lts",
        help=(
            "Node.js version to use for repo-local submission tooling. "
            "Use 'lts' or an exact version like 'v22.15.0'."
        ),
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap local draft-render dependencies for this draft repo.")
    subparsers = parser.add_subparsers(dest="command")

    bootstrap = subparsers.add_parser(
        "bootstrap",
        help="Bootstrap the local i-d-template checkout and render this draft repo.",
    )
    add_wsl_arguments(bootstrap)
    add_submission_arguments(bootstrap)
    bootstrap.set_defaults(func=command_bootstrap)

    status = subparsers.add_parser(
        "status",
        help="Report whether this draft repo is ready for rendering and pre-submit validation.",
    )
    status.set_defaults(func=command_status)

    validate_submission = subparsers.add_parser(
        "validate-submission",
        help="Build the next versioned XML and run repo-local idnits validation from this repo's local environment.",
    )
    add_wsl_arguments(validate_submission)
    add_submission_arguments(validate_submission)
    validate_submission.set_defaults(func=command_validate_submission)

    args = parser.parse_args(argv)
    if args.command is None:
        args.command = "bootstrap"
        args.func = command_bootstrap
        args.use_wsl = False
        args.install_wsl_deps = False
        args.wsl_distro = None
        args.submission_tools = False
        args.node_version = "lts"
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
