# JSON Baseline Encoding Direction

This note tracks the working direction for the participant-facing baseline
message encoding in the protocol draft.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

Use JSON as the baseline participant-facing encoding.

Do not make CBOR part of the baseline protocol or a mandatory-to-implement
alternate encoding at this stage.

If there is later demonstrated need from a real direct-participant device class
that can otherwise satisfy the minimum PPD lifecycle and security model, the
draft may later define a profiled alternate compact encoding.

### Why This Direction Holds

- PPD is control-plane traffic rather than high-rate telemetry
- the expensive parts for constrained devices are more likely to be security,
  identity, lifecycle handling, and policy logic than JSON parsing alone
- adding a second baseline encoding would multiply the conformance surface,
  examples, testing burden, and interoperability risk
- compact identifiers and disciplined object shapes already recover most of the
  practical payload-size benefit without adding a second representation model
- devices too constrained to implement the minimum participant-facing protocol
  hooks directly are likely better modeled through an intermediary than by
  bending the direct protocol around them

### Participant-Model Boundary

The baseline participant-facing encoding should be designed for devices and
services that are capable enough to implement the minimum direct-participant
contract:

- discovery confirmation
- registration
- declaration
- policy retrieval
- acknowledgement
- the applicable security hooks for their profile

Devices below that threshold should not drive the baseline wire-format choice.

Those ecosystems may still participate indirectly through a local gateway, hub,
or backend service that speaks the direct participant-facing protocol on their
behalf.

### Relationship To The Compact-Identifier Decision

The JSON baseline decision does not weaken the compact-term direction.

The intended combination is:

- JSON as the baseline wire encoding
- compact taxonomy identifiers on the wire
- stable namespace-based identifiers behind the compact form
- strict object-shape definition in the draft

That keeps the participant-facing messages readable and simple while avoiding
the semantic looseness of unscoped free-form strings.

### Namespace Detail: The Minimum Necessary Scope

We do not need a heavy namespace machinery story in the draft.

We do need enough detail to ensure:

- compact taxonomy terms do not collide across vendors or extensions
- an implementation can expand a compact term deterministically
- extension terms remain separable from the core vocabulary
- unknown-term handling is not left to guesswork

The draft therefore only needs a minimal namespace discipline, not full
linked-data processing or a rich ontology-exchange model in every message.

### What To Avoid In The Draft

- do not optimize the baseline encoding around devices that are too constrained
  to be direct participants
- do not add CBOR as a baseline requirement without a demonstrated direct-
  participant need
- do not assume JSON means the schema can stay loose or stringly typed
- do not let namespace handling grow into a heavy processing model that small
  participants cannot implement

### Cohesive Draft Story

The draft should tell the encoding story in this sequence:

1. the baseline participant-facing protocol uses JSON
2. PPD is a low-frequency control plane, not a byte-critical telemetry plane
3. payload compactness comes first from disciplined message design rather than
   alternate encodings
4. direct participants must meet a minimum lifecycle and security threshold
5. devices below that threshold are better represented indirectly
6. compact taxonomy identifiers still need a minimal deterministic namespace
   story so the JSON remains interoperable

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline participant-facing protocol uses JSON. PPD is a low-frequency
control plane, so the draft should prioritize compact schema design over adding
CBOR or another alternate baseline encoding. Devices too constrained to
implement the minimum direct-participant lifecycle and security hooks should be
represented indirectly rather than forcing the baseline protocol to optimize
around them. The draft only needs enough namespace detail to make compact
taxonomy identifiers deterministic and interoperable."
