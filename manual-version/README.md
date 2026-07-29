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
|   |-- resume.html.j2               # semantic document structure
|   |-- resume.css                   # professional screen and print design
|   `-- requirements.txt             # Python dependencies
|-- resume_tool.py                   # renderer; kept here for existing applications
|-- New-Application.cmd              # interactive application wizard
|-- Render-Master.cmd                # rebuild the master outputs
|-- index.html                       # rendered master preview
`-- Ehsan-Sharafian-Resume.pdf       # rendered master PDF
```

The editable content, HTML structure, and CSS design remain separate at the
source level. During rendering, CSS is embedded into `index.html`, so generated
application folders do not need a separate stylesheet. Company, role, URL,
date, and status are stored in the `application` section of `resume.yaml`, so a
separate notes file is not required.

## One-time setup

Open Command Prompt in `manual-version`:

```cmd
python -m pip install -r system\requirements.txt
```

Microsoft Edge, Google Chrome, or Chromium is required for PDF generation. The
renderer automatically checks standard Windows installation locations.

## Create a job-specific resume interactively

Double-click:

```text
New-Application.cmd
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

After editing, double-click the application's `Render.cmd`. It regenerates its
HTML and PDF without changing the master or another application.

## Update the master

Edit:

```text
master\Ehsan_Sharafian_Master.yaml
```

Then double-click:

```text
Render-Master.cmd
```

This regenerates the top-level `index.html` and
`Ehsan-Sharafian-Resume.pdf`.

## Change the shared design

Edit:

```text
system\resume.css
```

Edit `system\resume.html.j2` only when changing the HTML document structure.
Existing application PDFs remain unchanged until their `Render.cmd` is run.

## Save applications to Git

From the repository root:

```cmd
git add manual-version
git commit -m "Add tailored manual resume"
git push
```

This repository is public. Do not store confidential information in
`resume.yaml`.
