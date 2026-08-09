# Custom YAML resume system

This directory turns resume information from YAML into a professional,
self-contained HTML file and a submission-ready PDF.

## Organized structure

```text
manual-version/
|-- master/
|   `-- Ehsan_Sharafian_Master.yaml  # complete resume information
|-- applications/
|   `-- YYYY/
|       `-- YYYY-MM-DD-company-role/
|           |-- resume.yaml          # tailored information and job metadata
|           |-- index.html           # self-contained HTML with embedded style
|           |-- resume.pdf           # submission version
|           `-- Render.cmd           # rebuild this application
|-- system/
|   |-- resume_tool.py               # renderer and application wizard
|   |-- resume.html.j2               # semantic document structure
|   |-- resume.css                   # professional screen and print design
|   |-- index.html                   # rendered master preview
|   `-- requirements.txt             # Python dependencies
|-- New-Application.cmd              # interactive application wizard (Windows)
|-- New-Application.command          # interactive application wizard (macOS/Linux)
|-- Render-Master.cmd                # rebuild the master outputs (Windows)
|-- Render-Master.command           # rebuild the master outputs (macOS/Linux)
`-- Ehsan-Sharafian-Resume.pdf       # rendered master PDF
```

## Cross-platform launchers

Every launcher ships in two forms that do exactly the same thing:

- `*.cmd` — double-click on **Windows**.
- `*.command` — double-click in **Finder** on **macOS** (also runnable from a
  terminal on macOS or Linux).

Both call the same `system/resume_tool.py`, so the HTML and PDF come out
identical regardless of which computer you use. Each new application folder
gets both a `Render.cmd` and a `Render.command`. The Python tool already knows
where to find Microsoft Edge, Google Chrome, or Chromium on Windows and macOS
for PDF generation.

On macOS the first time you double-click a `.command` file, Gatekeeper may ask
for confirmation; choose **Open**. If a `.command` file ever loses its
executable flag (for example after copying it around), restore it with
`chmod +x <file>.command` from a terminal.

The editable content, HTML structure, and CSS design remain separate at the
source level. During rendering, CSS is embedded into `index.html`, so generated
application folders do not need a separate stylesheet. Company, role, URL,
date, and status are stored in the `application` section of `resume.yaml`, so a
separate notes file is not required.

## One-time setup

On **Windows**, open Command Prompt in `manual-version`:

```cmd
python -m pip install -r system\requirements.txt
```

On **macOS/Linux**, open a terminal in `manual-version`:

```bash
python3 -m pip install -r system/requirements.txt
```

Microsoft Edge, Google Chrome, or Chromium is required for PDF generation. The
renderer automatically checks standard Windows and macOS installation
locations.

## Create a job-specific resume interactively

Double-click the launcher for your system:

```text
New-Application.cmd        (Windows)
New-Application.command    (macOS)
```

The wizard asks for:

1. company name;
2. role or position title;
3. job URL;
4. application date;
5. whether to generate a PDF immediately;
6. confirmation before creating anything.

The window remains open after completion so messages and errors can be read.

Command-line mode is also supported:

```cmd
New-Application.cmd -Company "Medtronic" -Role "Biomechanics Engineer" -JobUrl "https://example.com/job/12345"
```

```bash
./New-Application.command -Company "Medtronic" -Role "Biomechanics Engineer" -JobUrl "https://example.com/job/12345"
```

## Tailor and re-render an application

Open the generated application's `resume.yaml`. Change only the content needed
for that job:

- rewrite `resume.summary`;
- reorder or rewrite `resume.skills`;
- prioritize relevant experience and highlights;
- remove content that does not support the role;
- keep all claims and metrics accurate.

The application metadata is at the top:

```yaml
application:
  company: Medtronic
  role: Biomechanics Engineer
  job_url: https://example.com/job/12345
  created: 2026-07-29
  status: Preparing
```

After editing, double-click the application's `Render.cmd` (Windows) or
`Render.command` (macOS). It regenerates its HTML and PDF without changing the
master or another application.

## Update the master

Edit:

```text
master\Ehsan_Sharafian_Master.yaml
```

Then double-click the launcher for your system:

```text
Render-Master.cmd        (Windows)
Render-Master.command    (macOS)
```

This regenerates `system/index.html` and the top-level
`Ehsan-Sharafian-Resume.pdf`.

## Change the shared design

Edit:

```text
system\resume.css
```

Edit `system\resume.html.j2` only when changing the HTML document structure.
Existing application PDFs remain unchanged until their `Render.cmd` (Windows) or
`Render.command` (macOS) is run.

## Save applications to Git

From the repository root:

```cmd
git add manual-version
git commit -m "Add tailored manual resume"
git push
```

This repository is public. Do not store confidential information in
`resume.yaml`.
