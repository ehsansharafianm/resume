# Custom YAML resume system

This directory is a small, independent resume publishing system. Resume
information lives in YAML, document structure lives in a Jinja HTML template,
and visual design lives in CSS.

## Architecture

```text
manual-version/
|-- master/
|   `-- Ehsan_Sharafian_Master.yaml  # complete source of truth
|-- templates/
|   `-- resume.html.j2               # semantic HTML structure
|-- styles/
|   `-- resume.css                   # screen and print design
|-- applications/
|   `-- YYYY/
|       `-- YYYY-MM-DD-company-role/
|           |-- resume.yaml          # tailored content
|           |-- index.html           # rendered browser version
|           |-- resume.css           # style snapshot
|           |-- resume.pdf           # submission version
|           |-- job.md               # requirements and status
|           `-- Render.cmd           # re-render this application
|-- resume_tool.py                   # renderer and folder generator
|-- New-Application.cmd
`-- Render-Master.cmd
```

The YAML files contain information only. They do not contain page markup or
visual styling. The Jinja template determines document structure, while the CSS
controls typography, spacing, color, print size, and page-break behavior.

## One-time setup

Open Command Prompt in `manual-version` and install the renderer dependencies:

```cmd
python -m pip install -r requirements.txt
```

Microsoft Edge, Google Chrome, or Chromium is required for automatic PDF
generation. The renderer detects standard Windows installation locations.

## Update and render the master

Edit:

```text
master\Ehsan_Sharafian_Master.yaml
```

Then run:

```cmd
Render-Master.cmd
```

This regenerates the repository's main `index.html`, `resume.css`, and
`Ehsan-Sharafian-Resume.pdf`.

## Create a job-specific resume

For example:

```cmd
New-Application.cmd -Company "Medtronic" -Role "Biomechanics Engineer" -JobUrl "https://example.com/job/12345"
```

The command creates a dated folder under `applications`, copies the master
YAML, records the company and role, and renders HTML and PDF immediately.

Only edit the new application's `resume.yaml` when tailoring:

- rewrite `resume.summary`;
- reorder or rewrite entries under `resume.skills`;
- reorder experience and highlights;
- remove content that does not support the target role;
- preserve accurate claims and metrics.

After editing, run the `Render.cmd` inside that application folder:

```cmd
Render.cmd
```

Its HTML, CSS, and PDF are regenerated without changing the master or another
application.

## Create multiple versions

Run `New-Application.cmd` once per position. Every application is isolated:

```text
applications\2026\2026-07-29-medtronic-biomechanics-engineer
applications\2026\2026-07-30-boston-scientific-research-engineer
applications\2026\2026-08-02-stryker-senior-r-and-d-engineer-10452
```

If company, role, and date would create the same folder name, add the job ID to
the role.

## Change the design

Edit `styles\resume.css` to change typography, colors, margins, spacing, or
print behavior. Edit `templates\resume.html.j2` only when changing document
structure.

Existing application PDFs remain unchanged until their local `Render.cmd` is
run again. This preserves the exact version previously submitted.

## Save applications to Git

From the repository root:

```cmd
git add manual-version
git commit -m "Add tailored manual resume"
git push
```

This repository is public. Do not store confidential recruiter notes or
interview details in `job.md`.
