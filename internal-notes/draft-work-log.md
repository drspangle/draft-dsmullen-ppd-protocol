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
- Clarified that the declaration baseline stays minimal for architectural
  reasons: registration carries identity, declaration carries descriptive
  assertions, and policy plus acknowledgment carry lifecycle-critical policy
  binding and freshness state.

## 2026-05-13

- Tightened discovery text so the protocol draft now makes configured or
  provisioned endpoint support the baseline discovery floor, requires
  `GET /ppd/v1/meta` confirmation for discovered candidates, and treats
  automatic local discovery mechanisms as optional profiles.
- Added explicit participant-facing security profiles, including the
  lower-assurance `compatibility` mode, two baseline direct-device
  authenticated profiles, and an extension backend-mediated profile.
- Defined the initial PPD-specific problem-type vocabulary and recommended HTTP
  status mappings on top of Problem Details.
- Added concrete JSON examples for Device Declaration, Effective Policy, and
  Policy Acknowledgment Objects.
- Added coarse comparison outcome categories while keeping conflict-resolution
  procedure outside the baseline participant-facing protocol.
- Synchronized the companion architecture and taxonomy drafts with this
  protocol direction, including explicit companion-draft references in the
  architecture text and a taxonomy model centered on compact identifiers,
  extension namespaces, and mapping back to shared core primitives.
- Re-checked Martin Thomson's upstream `i-d-template` setup and submission
  guidance against this repo's local notes and workflow files, then updated the
  tracked template-operations note with the verified tag-driven submission
  path, fallback manual paths, Datatracker email-selection behavior, and a
  session-local note that the host Ubuntu-on-WSL setup is real but was not
  visible from this Codex execution context.
- Replaced example taxonomy release strings that hard-coded the current
  taxonomy Internet-Draft revision with a generic release identifier
  (`ppd-core-2026-05`) so the examples do not drift every time the taxonomy
  draft is republished.
- Removed the lower-assurance `compatibility` profile from the normative
  protocol model. The current direction is that all conforming PPD
  participation is authenticated, while extremely constrained devices that
  cannot meet the minimum authenticated direct-participant bar are expected to
  participate indirectly through a trusted intermediary or remain
  non-participating.
- Added `internal-notes/trusted-intermediary-examples.md` to capture concrete
  intermediary classes, exclusion cases, and a concise criticism-response
  framing for extremely constrained devices that cannot participate directly.
- Refined the comparison-outcome model so that, when a deployment exposes a
  comparison result at the baseline participant-facing protocol boundary, it is
  carried as an optional declaration-path Comparison Outcome Object rather than
  being overloaded into policy retrieval or acknowledgment.
- Renamed the Service Metadata Object field from `taxonomy_versions` to
  `supported_taxonomy_releases` so the metadata surface matches the newer
  taxonomy model, where release identifiers are secondary validation context
  rather than the primary semantic hook.
- Tightened the declaration-path comparison model so it is explicitly
  diagnostic only: no metadata flag, no participant-controlled request hook,
  and no baseline bargaining or homeowner-prompt channel through comparison
  outcomes.
- Tightened the security-profile naming so the metadata field is now
  `security_profile` and the profile identifiers are `direct-constrained`,
  `direct-certificate`, and `backend-mediated`, with authenticated
  participation treated as the baseline assumption rather than repeated in
  every profile token.
- Added `internal-notes/operation-response-shapes-direction.md` to capture the
  response-shape cleanup, including the decision that registration success
  should return only a canonical `device_id` and the remaining declaration and
  acknowledgment success-response questions.

## 2026-05-18

- Tightened the protocol draft's successful response bodies so the draft is no
  longer materially more precise on request objects than on response objects.
- Changed registration success to require an explicit Registration Result
  Object carrying only the canonical `device_id`, removing the earlier wording
  that allowed registration success to repeat metadata-confirmation fields.
- Changed declaration success so the baseline no-payload case uses
  `204 No Content`, while declaration responses that expose comparison results
  use `200 OK` with a Comparison Outcome Object.
- Changed acknowledgment success to require an explicit Acknowledgment Result
  Object carrying resulting association state plus exactly one freshness field
  (`renew_by` or `renewal_interval`).
- Added normative object definitions for Registration Result Object and
  Acknowledgment Result Object, plus a concrete acknowledgment-result example.
- Updated the response-shapes direction note so its resolved declaration and
  acknowledgment decisions match the normative draft text.
- Tightened compact taxonomy term processing so the draft now requires
  deterministic expansion, reserves `ppd` as the baseline core prefix, and
  requires explicit non-core prefix declarations when non-core compact terms
  appear.
- Clarified the participant-facing distinction between
  `term-resolution-failed` and `unsupported-taxonomy-term` so malformed or
  undeclared compact identifiers are separated from resolved-but-unsupported
  terms.
- Tightened the repo-local draft bootstrap contract so it now distinguishes
  render readiness from submission readiness, can optionally provision a
  repo-local Node.js toolchain under `.tooling/` for `idnits`, and exposes an
  explicit `validate-submission` command for `make next` plus enforced
  repo-local `idnits` validation.
- Defined the baseline `policy_hash` computation so it is now interoperable:
  the hash covers the Effective Policy Object serialized as canonical JSON per
  RFC 8785, with the `policy_hash` member itself omitted from the hashed form.
- Defined the minimum renewal procedure explicitly as effective-policy retrieval
  followed, when the current policy instance is unchanged, by a fresh
  acknowledgment of that same instance; if the returned policy instance differs
  or the service returns `reassociation-required`, renewal escalates to
  reassociation.
