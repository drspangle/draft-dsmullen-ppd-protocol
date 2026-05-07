# Template Operations

These notes summarize how this repository uses Martin Thomson's
`i-d-template` tooling.

## Repository Shape

- Draft source: `draft-dsmullen-ppd-protocol.md`
- Rendered outputs are ignored by git.
- `internal-notes/` is for local notes only and is excluded from the editor's
  copy workflow trigger.

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