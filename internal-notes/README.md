# Internal Notes

These notes are local to this repository and are intentionally kept separate
from the functional draft contents.

Use these files for:

- protocol-draft editorial history
- local build and publication commands
- source-material pointers into `habanero-dev`
- open drafting questions that are not yet ready to become Internet-Draft text

Do not put protocol semantics here if they belong in the draft itself.

## Files

- `draft-work-log.md`: running log of protocol-draft changes and review findings
- `discovery-profile-direction.md`: working direction for the protocol-draft
  discovery model and the edits needed to carry it into draft text
- `security-profile-direction.md`: working direction for the protocol-draft
  security profiles, conformance floor, and participant-model scoping
- `taxonomy-binding-direction.md`: working direction for the protocol-draft
  boundary between message schema stability and taxonomy extensibility
- `term-identifier-encoding-direction.md`: working direction for compact
  taxonomy term identifiers and the gaps exposed by the current Habanero shape
- `json-baseline-encoding-direction.md`: working direction for keeping JSON as
  the baseline participant-facing encoding and scoping namespace detail to the
  minimum needed for interoperable compact term identifiers
- `acknowledgment-semantics-direction.md`: working direction for treating the
  baseline policy acknowledgment as a receipt signal rather than a compliance or
  compatibility claim
- `policy-conflict-outcomes-direction.md`: working direction for defining only
  coarse conflict outcome categories, while keeping conflict resolution
  procedure outside the baseline participant protocol
- `association-state-direction.md`: working direction for standardizing the
  proven coarse association-state vocabulary while keeping richer dashboard and
  operator enrichments optional
- `error-model-direction.md`: working direction for using standard HTTP problem
  details plus a small PPD-specific problem vocabulary, without stretching HTTP
  status semantics or inventing a custom error envelope
- `template-operations.md`: local render and eventual publication workflow notes
- `source-material.md`: protocol-relevant design artifacts in `habanero-dev`
- `scripts/`: local WSL helper scripts copied from the architecture repo
