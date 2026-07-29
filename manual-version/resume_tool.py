from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
    from markupsafe import Markup
    from ruamel.yaml import YAML
except ImportError as exc:
    raise SystemExit(
        "Missing renderer dependencies. Run:\n"
        '  python -m pip install -r requirements.txt'
    ) from exc


PROJECT_ROOT = Path(__file__).resolve().parent
SYSTEM_ROOT = PROJECT_ROOT / "system"
DEFAULT_TEMPLATE = SYSTEM_ROOT / "resume.html.j2"
DEFAULT_STYLESHEET = SYSTEM_ROOT / "resume.css"
DEFAULT_MASTER = PROJECT_ROOT / "master" / "Ehsan_Sharafian_Master.yaml"


class ResumeError(RuntimeError):
    pass


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ResumeError(f"YAML file not found: {path}")

    yaml = YAML(typ="safe")
    with path.open("r", encoding="utf-8") as stream:
        data = yaml.load(stream)

    if not isinstance(data, dict):
        raise ResumeError(f"Expected a YAML mapping in {path}")
    if not isinstance(data.get("resume"), dict):
        raise ResumeError(f"Missing required 'resume' mapping in {path}")

    required = ("name", "summary", "education", "skills", "experience")
    missing = [key for key in required if key not in data["resume"]]
    if missing:
        raise ResumeError(f"Missing required resume fields: {', '.join(missing)}")

    data.setdefault("application", {})
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 110
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        yaml.dump(data, stream)


def richtext(value: Any) -> Markup:
    escaped = html.escape(str(value), quote=False)
    formatted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return Markup(formatted)


def render_html(
    input_yaml: Path,
    output_html: Path,
    template_path: Path = DEFAULT_TEMPLATE,
    stylesheet_path: Path = DEFAULT_STYLESHEET,
) -> None:
    data = load_yaml(input_yaml)

    if not template_path.is_file():
        raise ResumeError(f"HTML template not found: {template_path}")
    if not stylesheet_path.is_file():
        raise ResumeError(f"Stylesheet not found: {stylesheet_path}")

    environment = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(("html", "xml")),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    environment.filters["richtext"] = richtext
    template = environment.get_template(template_path.name)

    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(
        template.render(**data, stylesheet=stylesheet),
        encoding="utf-8",
        newline="\n",
    )


def find_browser(explicit_browser: str | None = None) -> Path:
    candidates: list[Path] = []

    if explicit_browser:
        candidates.append(Path(explicit_browser))

    for executable in ("msedge", "msedge.exe", "chrome", "chrome.exe", "chromium"):
        located = shutil.which(executable)
        if located:
            candidates.append(Path(located))

    if sys.platform == "win32":
        candidates.extend(
            [
                Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
                Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
                Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
                Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            ]
        )
    elif sys.platform == "darwin":
        candidates.extend(
            [
                Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
            ]
        )

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    raise ResumeError(
        "Microsoft Edge, Google Chrome, or Chromium was not found. "
        "Install one of them or render with --skip-pdf."
    )


def render_pdf(
    input_html: Path,
    output_pdf: Path,
    browser_path: str | None = None,
) -> None:
    browser = find_browser(browser_path)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    temporary_pdf = output_pdf.with_name(f".{output_pdf.stem}.rendering.pdf")
    if temporary_pdf.exists():
        temporary_pdf.unlink()

    with tempfile.TemporaryDirectory(prefix="resume-browser-") as profile:
        command = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--hide-scrollbars",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={temporary_pdf.resolve()}",
            input_html.resolve().as_uri(),
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            check=False,
        )

    if result.returncode != 0:
        temporary_pdf.unlink(missing_ok=True)
        details = (result.stderr or result.stdout).strip()
        raise ResumeError(
            f"Browser PDF rendering failed with exit code {result.returncode}.\n{details}"
        )
    if not temporary_pdf.is_file() or temporary_pdf.stat().st_size < 1000:
        temporary_pdf.unlink(missing_ok=True)
        raise ResumeError(f"Browser did not create a valid PDF: {output_pdf}")

    temporary_pdf.replace(output_pdf)


def render_resume(
    input_yaml: Path,
    output_html: Path,
    output_pdf: Path | None,
    template_path: Path = DEFAULT_TEMPLATE,
    stylesheet_path: Path = DEFAULT_STYLESHEET,
    browser_path: str | None = None,
) -> None:
    render_html(input_yaml, output_html, template_path, stylesheet_path)
    if output_pdf is not None:
        render_pdf(output_html, output_pdf, browser_path)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    if not slug:
        raise ResumeError(f"Could not create a folder-safe name from {value!r}")
    return slug


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ResumeError("Application date must use YYYY-MM-DD format.") from exc


def create_application(args: argparse.Namespace) -> None:
    application_date = parse_date(args.application_date)
    master_path = Path(args.master).resolve()
    destination_root = Path(args.destination_root).resolve()
    folder_name = (
        f"{application_date.isoformat()}-{slugify(args.company)}-{slugify(args.role)}"
    )
    application_folder = destination_root / str(application_date.year) / folder_name

    if application_folder.exists():
        raise ResumeError(
            f"Application folder already exists: {application_folder}\n"
            "Use a distinct role name or include the job ID."
        )

    application_folder.mkdir(parents=True)
    application_yaml = application_folder / "resume.yaml"
    shutil.copy2(master_path, application_yaml)

    data = load_yaml(application_yaml)
    data["application"] = {
        "company": args.company,
        "role": args.role,
        "job_url": args.job_url,
        "created": application_date.isoformat(),
        "status": "Preparing",
    }
    write_yaml(application_yaml, data)

    render_command = (
        "@echo off\n"
        'python "%~dp0..\\..\\..\\resume_tool.py" render '
        '-Input "%~dp0resume.yaml" '
        '-OutputHtml "%~dp0index.html" '
        '-OutputPdf "%~dp0resume.pdf" %*\n'
    )
    (application_folder / "Render.cmd").write_text(
        render_command, encoding="utf-8", newline="\r\n"
    )

    output_pdf = None if args.skip_pdf else application_folder / "resume.pdf"
    render_resume(
        application_yaml,
        application_folder / "index.html",
        output_pdf,
        browser_path=args.browser,
    )

    print("Application created successfully:")
    print(f"  {application_folder}")
    print("")
    print("Files:")
    print("  resume.yaml  - edit job-specific content here")
    print("  index.html   - self-contained browser preview")
    if output_pdf:
        print("  resume.pdf   - submission-ready PDF")
    print("  Render.cmd   - re-render after editing YAML")


def prompt_required(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This value is required. Please try again.")


def wizard_command(args: argparse.Namespace) -> int:
    print("=" * 60)
    print("            Create a tailored resume application")
    print("=" * 60)
    print("")
    print("This wizard copies your master YAML, creates a job folder,")
    print("and renders the custom HTML resume and PDF.")
    print("")

    company = prompt_required("Company name: ")
    role = prompt_required("Role or position title: ")
    job_url = input("Job URL (optional): ").strip()

    while True:
        application_date = input(
            "Application date YYYY-MM-DD (press Enter for today): "
        ).strip()
        if not application_date:
            application_date = date.today().isoformat()
            break
        try:
            parse_date(application_date)
            break
        except ResumeError as exc:
            print(exc)

    pdf_choice = input("Generate PDF now? [Y/n]: ").strip().lower()
    skip_pdf = pdf_choice in {"n", "no"}

    print("")
    print("-" * 60)
    print(f"Company: {company}")
    print(f"Role:    {role}")
    if job_url:
        print(f"URL:     {job_url}")
    print(f"Date:    {application_date}")
    print(f"PDF:     {'No - HTML only' if skip_pdf else 'Yes'}")
    print("-" * 60)
    print("")

    confirmation = input("Create this application? [Y/n]: ").strip().lower()
    if confirmation in {"n", "no"}:
        print("")
        print("Application creation cancelled.")
        input("Press Enter to close this window...")
        return 0

    create_args = argparse.Namespace(
        company=company,
        role=role,
        job_url=job_url,
        application_date=application_date,
        master=str(DEFAULT_MASTER),
        destination_root=str(PROJECT_ROOT / "applications"),
        browser=args.browser,
        skip_pdf=skip_pdf,
    )

    print("")
    try:
        create_application(create_args)
    except (ResumeError, OSError, subprocess.SubprocessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("")
        input("Press Enter to close this window...")
        return 1

    print("")
    print("Finished. Edit resume.yaml in the new application folder,")
    print("then run its Render.cmd whenever you want to rebuild it.")
    print("")
    input("Press Enter to close this window...")
    return 0


def render_command(args: argparse.Namespace) -> None:
    output_pdf = None if args.skip_pdf else Path(args.output_pdf).resolve()
    render_resume(
        Path(args.input).resolve(),
        Path(args.output_html).resolve(),
        output_pdf,
        browser_path=args.browser,
    )
    print(f"Generated HTML: {Path(args.output_html).resolve()}")
    if output_pdf:
        print(f"Generated PDF:  {output_pdf}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render Ehsan Sharafian's YAML resume into HTML and PDF."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser(
        "create", help="Create and render a job-specific application folder."
    )
    create.add_argument("-Company", "--company", required=True)
    create.add_argument("-Role", "--role", required=True)
    create.add_argument("-JobUrl", "--job-url", default="")
    create.add_argument(
        "-ApplicationDate",
        "--application-date",
        default=date.today().isoformat(),
        help="Application date in YYYY-MM-DD format.",
    )
    create.add_argument(
        "-Master",
        "--master",
        default=str(DEFAULT_MASTER),
        help="Master YAML source.",
    )
    create.add_argument(
        "-DestinationRoot",
        "--destination-root",
        default=str(PROJECT_ROOT / "applications"),
    )
    create.add_argument("-Browser", "--browser", default=None)
    create.add_argument("-SkipPdf", "--skip-pdf", action="store_true")
    create.set_defaults(handler=create_application)

    wizard = subparsers.add_parser(
        "wizard", help="Open an interactive job-application wizard."
    )
    wizard.add_argument("-Browser", "--browser", default=None)
    wizard.set_defaults(handler=wizard_command)

    render = subparsers.add_parser(
        "render", help="Render one YAML resume into HTML and PDF."
    )
    render.add_argument("-Input", "--input", required=True)
    render.add_argument("-OutputHtml", "--output-html", required=True)
    render.add_argument("-OutputPdf", "--output-pdf", default="resume.pdf")
    render.add_argument("-Browser", "--browser", default=None)
    render.add_argument("-SkipPdf", "--skip-pdf", action="store_true")
    render.set_defaults(handler=render_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.handler(args)
    except (ResumeError, OSError, subprocess.SubprocessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())
