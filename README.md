<!-- regenerate: on (set to off if you edit this file) -->

# Privacy Preference Declaration Protocol Specification

This is the working area for the individual Internet-Draft, "Privacy Preference Declaration Protocol Specification".

* [Editor's Copy](https://drspangle.github.io/draft-dsmullen-ppd-protocol/#go.draft-dsmullen-ppd-protocol.html)
* [Datatracker Page](https://datatracker.ietf.org/doc/draft-dsmullen-ppd-protocol/)
* [Individual Draft](https://datatracker.ietf.org/doc/html/draft-dsmullen-ppd-protocol)
* [Compare Editor's Copy to Individual Draft](https://drspangle.github.io/draft-dsmullen-ppd-protocol/#go.draft-dsmullen-ppd-protocol.diff)

Use this repository for the draft source, local render workflow, and local
working notes for this draft only.

## Workstation Bootstrap

This repository owns its own draft-render setup. Bootstrap it with:

```sh
python3 scripts/setup_draft_workstation.py bootstrap
```

There is intentionally no shared workspace bootstrap. This bootstrap configures
only this repository.

Validation steps for this repository are in [WORKSTATION-VALIDATION.md](WORKSTATION-VALIDATION.md).

## Related Drafts

- architecture draft source: [draft-dsmullen-ppd-architecture](https://github.com/drspangle/draft-dsmullen-ppd-architecture)
- architecture draft Datatracker page: [draft-dsmullen-ppd-architecture](https://datatracker.ietf.org/doc/draft-dsmullen-ppd-architecture)
- taxonomy draft source: [draft-dsmullen-ppd-taxonomy](https://github.com/drspangle/draft-dsmullen-ppd-taxonomy)
- taxonomy draft Datatracker page: [draft-dsmullen-ppd-taxonomy](https://datatracker.ietf.org/doc/draft-dsmullen-ppd-taxonomy)

## Start Here

1. Bootstrap the local render workflow with `python3 scripts/setup_draft_workstation.py bootstrap`.
2. Validate the local setup with [WORKSTATION-VALIDATION.md](WORKSTATION-VALIDATION.md).
3. Build the draft with `make`.
4. Use [internal-notes/README.md](internal-notes/README.md) for local working notes.

On Windows, prefer native POSIX tooling when available. Use WSL only as an
explicit fallback:

```powershell
py -3 scripts\setup_draft_workstation.py bootstrap --use-wsl --install-wsl-deps
```

## Contributing

See the
[guidelines for contributions](https://github.com/drspangle/draft-dsmullen-ppd-protocol/blob/main/CONTRIBUTING.md).

Contributions can be made by creating pull requests.
The GitHub interface supports creating pull requests using the Edit (✏️) button.

## Command Line Usage

Formatted text and HTML versions of the draft can be built using `make`.

```sh
$ make
```

Command line usage requires that you have the necessary software installed. See
[the instructions](https://github.com/martinthomson/i-d-template/blob/main/doc/SETUP.md).
