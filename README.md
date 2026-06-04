# SlingShot IT Security Toolkit

**SlingShot** is a Python-based IT security and system management toolkit built with `tkinter` and `customtkinter`. The project is being rebooted and cleaned up so it can become a reliable local-first admin/helpdesk/security utility instead of a loose collection of disconnected tools.

## Current status

The app currently lives in `slingshot3/` and includes a large set of tools across security, monitoring, utilities, networking, backups, advanced system checks, IT support, and reconnaissance.

The immediate goal is stability first:

- clean dependency management
- repeatable setup
- smoke checks before large changes
- safer config defaults
- clearer upgrade path
- better separation between UI, tool metadata, and tool execution

## Repo layout

```text
.
├── README.md
├── requirements.txt
├── required dependencies
└── slingshot3/
    ├── config.json
    ├── custom_tools.py
    ├── slingshot.py
    ├── smoke_check.py
    └── tools.py
```

## Setup

Use a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Some Windows-specific tools may require extra Windows packages or admin rights depending on the feature being used.

## Run the app

```powershell
python .\slingshot3\slingshot.py
```

## Run the smoke check

```powershell
python .\slingshot3\smoke_check.py
```

The smoke check validates the repo layout, required Python modules, and basic config sanity without launching the GUI.

## Upgrade plan

The next serious pass should focus on these items:

1. Move tool metadata into a dedicated registry file.
2. Stop importing all optional and Windows-only packages at module load.
3. Add safe wrappers for admin-only actions.
4. Replace simulated or weak tools with real local checks or mark them disabled.
5. Modernize the UI around a dashboard/sidebar/card layout.
6. Add run history, exportable triage reports, and safer confirmation flows.
7. Keep the project local-first and avoid paid services or hosted dependencies.

## Validation rule

Do not call a phase complete unless there is proof:

- changed files are listed
- smoke check was run
- failures are documented
- the diff shows meaningful changes
- risky or system-changing tools are clearly marked

## Notes for future AI/Codex work

When using an AI coding agent on this repo, require it to:

- name exact file targets before editing
- make real code changes, not just describe them
- run the smoke check after edits
- provide a diff summary
- fail loudly if it cannot validate the work
