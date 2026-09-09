from __future__ import annotations

import shlex
import subprocess
import tarfile
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import questionary
import typer

app = typer.Typer(help="GraphOntology command-line interface.", no_args_is_help=True)


@app.callback()
def callback() -> None:
    """GraphOntology CLI root."""
    return None


def _ask_required_text(message: str, default: str | None = None) -> str:
    while True:
        answer = questionary.text(message, default=default or "").ask()
        if answer is None:
            raise typer.Abort()
        cleaned = answer.strip()
        if cleaned:
            return cleaned
        typer.echo("This value is required.")


def _download_archive(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Downloading package from {url}")
    request = Request(url, headers={"User-Agent": "graphontology-cli/0.0.1"})
    chunk_size = 1024 * 1024  # 1 MiB
    with urlopen(request) as response:
        content_length = response.headers.get("Content-Length")
        total_bytes = int(content_length) if content_length and content_length.isdigit() else None

        with destination.open("wb") as output_file:
            if total_bytes is not None:
                with typer.progressbar(
                    length=total_bytes,
                    label="Downloading",
                    show_percent=True,
                    show_pos=True,
                ) as progress:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        output_file.write(chunk)
                        progress.update(len(chunk))
            else:
                downloaded = 0
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    output_file.write(chunk)
                    downloaded += len(chunk)
                    typer.echo(
                        f"\rDownloading: {downloaded / (1024 * 1024):.1f} MiB",
                        nl=False,
                    )
                typer.echo("")
    typer.echo(f"Saved archive to {destination}")


def _extract_tar_gz(archive_path: Path, extract_to: Path) -> None:
    extract_to.mkdir(parents=True, exist_ok=True)
    typer.echo(f"Extracting {archive_path} into {extract_to}")
    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():
            member_path = (extract_to / member.name).resolve()
            if extract_to.resolve() not in member_path.parents and member_path != extract_to.resolve():
                raise ValueError(f"Blocked unsafe archive member path: {member.name}")
        tar.extractall(path=extract_to)
    typer.echo("Extraction completed.")


def _find_sql_dump(extract_dir: Path, requested_dump: str) -> Path:
    if requested_dump:
        dump_path = Path(requested_dump).expanduser()
        if not dump_path.is_absolute():
            dump_path = extract_dir / dump_path
        if dump_path.exists() and dump_path.is_file():
            return dump_path.resolve()
        raise FileNotFoundError(f"Dump file not found: {dump_path}")

    sql_candidates = sorted(extract_dir.rglob("*.sql"))
    if not sql_candidates:
        raise FileNotFoundError(f"No .sql files found under {extract_dir}")
    if len(sql_candidates) == 1:
        return sql_candidates[0].resolve()

    choices = [str(path.relative_to(extract_dir)) for path in sql_candidates]
    selected = questionary.select(
        "Multiple SQL dumps found. Select the one to import:",
        choices=choices,
    ).ask()
    if selected is None:
        raise typer.Abort()
    return (extract_dir / selected).resolve()


@app.command("init")
def init_command() -> None:
    """
    Run interactive initialization wizard:
    download package, unpack tar.gz, and run an import command.
    """
    typer.echo("GraphOntology initialization wizard")

    package_url = _ask_required_text("Package URL (.tar.gz)")
    parsed = urlparse(package_url)
    default_archive_name = Path(parsed.path).name or "package.tar.gz"
    download_dir = _ask_required_text("Download directory", default="./data/downloads")
    archive_name = _ask_required_text("Archive file name", default=default_archive_name)
    extract_dir = _ask_required_text("Extraction directory", default="./data/import")
    dump_hint = questionary.text(
        "SQL dump path inside extracted folder (leave empty for auto-detect)",
        default="",
    ).ask()
    if dump_hint is None:
        raise typer.Abort()

    default_import_cmd = 'python -m graphontology.init_ontology_tables --dump "{dump_file}"'
    import_command_template = _ask_required_text(
        "Import command template (use {dump_file})",
        default=default_import_cmd,
    )

    archive_path = (Path(download_dir).expanduser() / archive_name).resolve()
    extract_path = Path(extract_dir).expanduser().resolve()
    dump_hint = dump_hint.strip()

    typer.echo("\nConfiguration summary:")
    typer.echo(f"  URL: {package_url}")
    typer.echo(f"  Archive path: {archive_path}")
    typer.echo(f"  Extract dir: {extract_path}")
    typer.echo(f"  Dump hint: {dump_hint or '(auto-detect)'}")
    typer.echo(f"  Import command: {import_command_template}")

    proceed = questionary.confirm("Proceed?", default=True).ask()
    if proceed is None or not proceed:
        raise typer.Abort()

    try:
        _download_archive(package_url, archive_path)
        _extract_tar_gz(archive_path, extract_path)
        dump_file = _find_sql_dump(extract_path, dump_hint)
        typer.echo(f"Using dump file: {dump_file}")

        command_text = import_command_template.format(dump_file=str(dump_file))
        typer.echo(f"Running import command: {command_text}")
        subprocess.run(shlex.split(command_text), check=True)
        typer.echo("Initialization completed successfully.")
    except Exception as exc:
        typer.echo(f"Initialization failed: {exc}", err=True)
        raise typer.Exit(code=1) from exc
