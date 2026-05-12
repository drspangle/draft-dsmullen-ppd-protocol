# Protocol Draft Work Log

This file records drafting work for `draft-dsmullen-ppd-protocol.md`.
It is not part of the rendered Internet-Draft.

## 2026-05-07

- Scaffolded this repository from the architecture-draft repository so it uses
  the same i-d-template workflow, GitHub Pages flow, and tag-driven publish
  workflow.
- Renamed the working draft source to `draft-dsmullen-ppd-protocol.md` and
  updated repository metadata and links for the new draft name.
- Seeded the initial protocol draft from the Habanero design materials,
  especially the device-facing API, discovery tradeoffs, lifecycle model,
  acknowledgment semantics, and security notes.
- Kept internal repository and operator-only surfaces out of the baseline
  protocol contract, except where they are mentioned explicitly as non-baseline
  or future work.
- Added `internal-notes/discovery-profile-direction.md` to capture the current
  decision and drafting story for a layered discovery profile before editing
  the normative draft text.
- Added `internal-notes/security-profile-direction.md` to capture the current
  decision on explicit security profiles, the authenticated participation
  accountability floor, and extension treatment for backend-mediated
  participation.
- Added `internal-notes/taxonomy-binding-direction.md` to capture the current
  decision that stable term identifiers, rather than a taxonomy version string
  alone, should be the primary semantic hook for extensible taxonomy-bearing
  protocol fields.
- Added `internal-notes/term-identifier-encoding-direction.md` to capture the
  decision to prefer compact taxonomy identifiers on the wire, together with a
  critical assessment of the current Habanero JSON shape and the follow-up
  gaps it exposes.
- Added `internal-notes/json-baseline-encoding-direction.md` to capture the
  decision to keep JSON as the baseline participant-facing encoding, defer
  CBOR unless a real direct-participant need emerges, and scope namespace
  detail to the minimum necessary for interoperable compact term identifiers.
- Refined `internal-notes/term-identifier-encoding-direction.md` to capture
  the narrower namespace decision: reserved core prefixes plus optional
  explicit extension-prefix declarations, without importing heavy JSON-LD or
  linked-data processing into the baseline participant model.
- Added `internal-notes/acknowledgment-semantics-direction.md` to capture the
  decision that baseline acknowledgment is a receipt for a specific policy
  instance, while participant-originated policy inputs, conflict handling,
  exceptions, and satisfiability remain separate concerns.
- Added `internal-notes/policy-conflict-outcomes-direction.md` to capture the
  decision to define only coarse conflict outcome categories in the baseline
  protocol and leave conflict-resolution procedure to household intent, policy
  behavior, device capability, and deployment logic.
- Added `internal-notes/association-state-direction.md` to capture the
  decision to standardize the Habanero prototype's coarse association-state
  vocabulary while keeping richer operator and dashboard enrichments optional.
- Added `internal-notes/error-model-direction.md` to capture the decision to
  use conventional HTTP status codes plus standard Problem Details with a
  small PPD-specific problem vocabulary, instead of inventing a custom error
  envelope or overloading HTTP status semantics.
- Added `internal-notes/policy-rule-shape-direction.md` to capture the
  decision that baseline declarations remain descriptive, effective policy
  remains normative, and baseline rule effects belong only in the
  household-originated policy object.
- Refined `internal-notes/policy-rule-shape-direction.md` to lock in `effect`
  as the preferred normative rule verdict field name, replacing the more
  ambiguous `decision` label used in current Habanero examples.
- Refined `internal-notes/policy-rule-shape-direction.md` to prefer atomic
  baseline rules with singular core dimensions, using multiple rules rather
  than array-valued baseline fields when several cases must be expressed.
- Refined `internal-notes/policy-rule-shape-direction.md` to include an
  explicit optional `constraints` object in the baseline rule shape, keeping
  the rule model simple while preserving a clear structured extension point for
  later qualifiers.
- Refined `internal-notes/policy-rule-shape-direction.md` to make `retention`
  and `locality` the preferred initial standardized `constraints` members, and
  to note that richer examples and fleshing-out material can stay in the repo
  even when the Internet-Draft keeps the normative text concise.

## 2026-05-12

- Added `internal-notes/protocol-narrative-direction.md` to capture the
  decision to tighten the draft's opening actor language and end-to-end story
  so that `PPD participant` is clearly device-side rather than a human
  household actor.
- Added `internal-notes/effective-policy-direction.md` to capture the
  distinction between association freshness and policy validity, support for
  company-specific taxonomies mapped to the core primitives, and the boundary
  between policy-instance provenance and collected-data provenance.
- Clarified that the protocol draft should defer most relationship-to-existing-
  work discussion to the architecture draft, with the protocol draft carrying
  only a short cross-reference to that broader comparison.
- Added `internal-notes/declaration-shape-direction.md` to capture the
  decision to replace flat declaration capability arrays with atomic
  descriptive statements, while leaving combination semantics to the taxonomy
  work.
- Refined the Effective Policy Object provenance naming to prefer
  `applied_policy_id` over the narrower `override_policy_id` label.
- Rewrote the draft opening sections to clarify the participant-facing
  narrative, actor language, and end-to-end lifecycle between the home-side PPD
  service endpoint and the device-side participant.
- Made the operations and message-object sections more explicit and normative by
  defining baseline object fields, compact term identifiers, taxonomy context,
  atomic policy rules with `effect`, optional structured `constraints`, and the
  Problem Details based error object.
- Refined the declaration model so a Device Declaration Object now carries a
  non-empty `statements` array of atomic descriptive cases instead of flat
  `supported_*` capability arrays, and generalized the shared constraints
  structure so both declaration statements and policy rules can use it.
