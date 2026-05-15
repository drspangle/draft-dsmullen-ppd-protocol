# Internal Notes

These notes are local to this repository and are intentionally kept separate
from the functional draft contents.

Use this README to decide which existing note file should absorb new protocol
draft work before creating another one.

Use these files for:

- protocol-draft editorial history
- local build and publication commands
- source-material pointers into the related gateway repository
- open drafting questions that are not yet ready to become Internet-Draft text

Do not put protocol semantics here if they belong in the draft itself.

## Start Here

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
- `policy-rule-shape-direction.md`: working direction for keeping baseline
  declarations descriptive, effective policy normative, and baseline rule
  effects scoped only to the household-originated policy object
- `protocol-narrative-direction.md`: working direction for the draft's
  end-to-end opening story, including clearer actor language that distinguishes
  device-side participants from human household actors
- `effective-policy-direction.md`: working direction for the baseline
  Effective Policy Object, including association-freshness semantics, mapped
  company-specific taxonomies, and the distinction between policy-instance
  provenance and collected-data provenance
- `declaration-shape-direction.md`: working direction for replacing flat
  declaration capability arrays with atomic descriptive statements while
  keeping combination semantics in the taxonomy work
- `operation-response-shapes-direction.md`: working direction for defining the
  remaining successful response bodies, including the minimal Registration
  Result Object and the open declaration/acknowledgment response questions
- `trusted-intermediary-examples.md`: concrete examples and criticism-response
  framing for what can count as a trusted intermediary for extremely
  constrained devices
- `template-operations.md`: local render and eventual publication workflow notes
- `source-material.md`: protocol-relevant design artifacts in the related gateway repository
- `scripts/`: local WSL helper scripts copied from the architecture repo
