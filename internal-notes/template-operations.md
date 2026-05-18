# Template Operations

These notes summarize how this repository uses Martin Thomson's
`i-d-template` tooling.

## Repository Shape

- Draft source: `draft-dsmullen-ppd-protocol.md`
- Rendered outputs are ignored by git.
- `internal-notes/` is for local notes only and is excluded from the editor's
  copy workflow trigger.

## Local Submission Validation

For this repository, pre-submit validation is a repo-local workflow, not a
shared workspace workflow.

Use the repository bootstrap first:

```sh
python3 scripts/setup_draft_workstation.py bootstrap --submission-tools
```

Then build the next versioned XML and run `idnits` with:

```sh
python3 scripts/setup_draft_workstation.py validate-submission
```

On native macOS, Linux, or Windows, the bootstrap command installs a repo-local
Node.js toolchain under `.tooling/` when `npm` is not already available.

## Local Rendering On Windows

Use Ubuntu under WSL for local rendering.

Render the editor's copy from PowerShell:

```powershell
wsl -d Ubuntu -- bash -lc "cd /mnt/c/Users/Daniel\ Smullen/Documents/draft-dsmullen-ppd-protocol && bash internal-notes/scripts/render-local-editor-copy.sh"
```

Run the local environment check:

```powershell
wsl -d Ubuntu -- bash -lc "cd /mnt/c/Users/Daniel\ Smullen/Documents/draft-dsmullen-ppd-protocol && bash internal-notes/scripts/check-template-env.sh"
```

Generate a local diff against the most recent tagged draft revision:

```powershell
wsl -d Ubuntu -- bash -lc "cd /mnt/c/Users/Daniel\ Smullen/Documents/draft-dsmullen-ppd-protocol && BUNDLE_PATH=/mnt/c/Users/Daniel\ Smullen/Documents/draft-dsmullen-ppd-protocol/lib/.gems make diff"
```

## Publishing Path

This repository is set up for the same tag-driven GitHub Actions submission
workflow used by the architecture draft.

When the repository exists on GitHub and the draft is ready:

```sh
git push origin main
git tag -a draft-dsmullen-ppd-protocol-00 -m "Submit draft-dsmullen-ppd-protocol-00"
git push origin draft-dsmullen-ppd-protocol-00
```

The publish workflow then runs `make upload` and Datatracker still requires the
normal confirmation email step.

## Upstream-Verified Submission Notes

These points were re-checked against Martin Thomson's upstream
`i-d-template` documentation on 2026-05-13:

- Local rendering on Windows is still expected to happen through WSL with a
  Linux distribution such as Ubuntu.
- The minimum local toolchain is POSIX `make`, `python3` with `pip` and
  `venv`, and `ruby` with `gem` and `bundler`. `npm` and `xmllint` are also
  expected by this repo's local pre-submit validation path. This repository's
  native bootstrap now provisions a repo-local Node.js toolchain under
  `.tooling/` when `npm` is missing.
- The preferred automated submission path is an annotated draft tag pushed to
  GitHub. For this repo that means:

```sh
git push origin main
git tag -a draft-dsmullen-ppd-protocol-00 -m "Submit draft-dsmullen-ppd-protocol-00"
git push origin draft-dsmullen-ppd-protocol-00
```

- The submitter email used by Datatracker needs to match a verified
  Datatracker account address. The template checks, in order:
  1. an `UPLOAD_EMAIL` value passed to the workflow;
  2. an exported `UPLOAD_EMAIL` value from the Makefile or environment;
  3. the email on an annotated git tag;
  4. the GitHub account email; and then
  5. the first author email in the draft.
- If CI submission fails because the draft needs fixing, delete the tag before
  retagging:

```sh
git tag -d draft-dsmullen-ppd-protocol-00
git push origin :draft-dsmullen-ppd-protocol-00
```

- If CI is unavailable, fallback paths are:
  - `make publish` after creating an annotated tag; or
  - `make next`, then manually submit the generated `.xml` file to
    Datatracker.

## Current Session Note

The host machine has Ubuntu installed and working under WSL. However, in this
Codex session, `wsl.exe -l -v` did not enumerate that distro. Treat that as an
execution-context limitation in this session, not a machine-level installation
problem.
