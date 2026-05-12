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
