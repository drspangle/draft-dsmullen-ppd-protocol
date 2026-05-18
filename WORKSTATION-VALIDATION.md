# Draft Workstation Validation

Use this runbook from a normal terminal, not from Codex.

This runbook validates this repository's local render setup and its native
pre-submit validation path.

## Scope

This runbook verifies that:

- the repo-local draft bootstrap works,
- the bootstrap remains idempotent when re-run,
- the draft can render locally from a normal terminal.
- the repo can build the next submission XML and run `idnits` from a normal
  terminal.

## Terminal

Run these commands from the repository root.

macOS and Linux:

```sh
cd /path/to/draft-dsmullen-ppd-protocol
python3 scripts/setup_draft_workstation.py status
python3 scripts/setup_draft_workstation.py bootstrap
python3 scripts/setup_draft_workstation.py status
python3 scripts/setup_draft_workstation.py bootstrap
make
python3 scripts/setup_draft_workstation.py bootstrap --submission-tools
python3 scripts/setup_draft_workstation.py status
python3 scripts/setup_draft_workstation.py validate-submission
```

Windows, native tooling first:

```powershell
cd C:\path\to\draft-dsmullen-ppd-protocol
py -3 scripts\setup_draft_workstation.py status
py -3 scripts\setup_draft_workstation.py bootstrap
py -3 scripts\setup_draft_workstation.py status
py -3 scripts\setup_draft_workstation.py bootstrap
make
py -3 scripts\setup_draft_workstation.py bootstrap --submission-tools
py -3 scripts\setup_draft_workstation.py status
py -3 scripts\setup_draft_workstation.py validate-submission
```

Windows, WSL only if native draft tooling is unavailable or broken:

```powershell
cd C:\path\to\draft-dsmullen-ppd-protocol
py -3 scripts\setup_draft_workstation.py bootstrap --use-wsl --install-wsl-deps
py -3 scripts\setup_draft_workstation.py validate-submission --use-wsl --install-wsl-deps
```

The first native `validate-submission` run may download a repo-local Node.js
toolchain into `.tooling/` and then fetch `idnits` through `npm`.

## Acceptance Criteria

- After `bootstrap`, `status` reports `Render outputs: present`.
- After `bootstrap`, `status` reports `Template checkout: present`.
- The second `bootstrap` completes without setup-only failures.
- `make` completes and updates the rendered draft output from a normal shell.
- The rendered HTML output exists at `draft-dsmullen-ppd-protocol.html`.
- After `bootstrap --submission-tools`, `status` reports `Submission prerequisites: ready`.
- `validate-submission` completes and updates `versioned/draft-dsmullen-ppd-protocol-00.xml`.
- `validate-submission` runs repo-local `idnits` validation successfully from a normal shell.

## Interpreting Failures

- If `bootstrap` fails, treat that as a workstation-setup problem first.
- If `bootstrap` succeeds but `make` fails on whitespace, lint, or draft
  content, treat that as a draft-content problem rather than a missing-toolchain
  problem.
- If render checks pass but `validate-submission` fails before `idnits`
  starts, treat that as a native submission-toolchain problem first.
- If `validate-submission` reaches `idnits` and then reports nits, treat
  that as a draft-quality problem rather than a missing-toolchain problem.
