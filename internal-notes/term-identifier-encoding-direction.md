# Term Identifier Encoding Direction

This note tracks the working direction for how taxonomy term identifiers should
appear on the wire in the participant-facing protocol.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

Use compact identifiers as the baseline participant-facing surface form, with a
defined mapping to stable namespace-based term identifiers.

The protocol should not require raw IRI-only term encoding in every
participant-facing JSON message.

At the same time, it should not leave taxonomy-bearing terms as unscoped local
strings.

The intended direction is:

- compact term identifiers are allowed as the normal wire form
- each compact term identifier maps deterministically to a stable namespace-
  based identifier defined by the taxonomy work
- the protocol defines a fixed core prefix set and allows optional extension
  prefix declarations when non-core terms appear
- taxonomy release metadata remains secondary validation context rather than the
  sole meaning hook

### Why This Direction Holds

- raw IRIs everywhere would be heavy and awkward for constrained or demo-facing
  participant JSON
- the Habanero demo already shows the practical value of readable compact terms
- bare strings without a namespace story do not scale to cross-vendor
  interoperability
- compact identifiers preserve readability while still allowing the protocol to
  anchor semantics on stable identifiers

### Critical Assessment Of The Current Habanero Shape

The current Habanero participant-facing shape is useful as a prototype surface
but too weak as a long-term semantic contract.

Current strengths:

- easy to read in JSON
- easy for simple clients to emit
- easy for dashboard and demo tooling to explain

Current weaknesses:

- taxonomy-bearing fields are bare strings with no namespace or identifier
  binding carried in the object
- policy objects carry a single `taxonomy_version`, but declarations do not
  carry an equivalent taxonomy binding
- there is no visible unknown-term or unsupported-term behavior in the current
  participant-facing contract
- the live `Rule` shape has no general extension slot such as `constraints`,
  despite the design notes already pointing toward richer rule qualifiers
- the repository currently computes effective policy by default-versus-override
  selection, not by real declaration-to-policy taxonomy matching
- metadata and registration responses still include prototype or internal
  artifacts that should not become long-term protocol assumptions

The practical consequence is that the current JSON shape generalizes as a demo
surface form more readily than it generalizes as a semantic interoperability
model.

### Boundary We Should Preserve

We should preserve:

- compact, readable participant-facing JSON
- stable protocol object shapes
- the ability for simple devices to emit declarations and consume policy
  without heavy ontology tooling

We should not preserve:

- unscoped local term strings as the only identifier model
- one policy-level taxonomy version field as the only semantic hook
- implicit acceptance of unknown terms
- prototype metadata fields that expose internal topology or placeholder
  authorization behavior

### Protocol Direction

The protocol should define:

- taxonomy-bearing fields carry compact identifiers
- those identifiers are interpreted against a defined namespace or vocabulary
  mapping
- the core protocol vocabulary uses reserved well-known prefixes
- extension vocabularies are introduced through explicit prefix declarations
  rather than through unscoped local strings
- the mapping from compact form to stable namespace-based identifier is
  deterministic and documented
- unknown-term behavior is explicit
- extension behavior is explicit

### Namespace Scope: Keep It Minimal

The draft does not need a heavy namespace-processing model.

It only needs enough machinery to ensure:

- core taxonomy terms are unambiguous across implementations
- extension terms do not collide with core terms or with each other
- an implementation can expand a compact identifier deterministically
- unknown or unmapped extension terms can be handled explicitly

The current working direction is therefore:

- reserve a fixed core prefix set in the protocol or companion taxonomy work
- require explicit inline declaration of non-core extension prefixes when such
  terms appear
- do not require full JSON-LD processing, remote context fetching, or general
  linked-data tooling in baseline participants

The taxonomy work should define:

- the canonical namespace-based term identifiers
- which compact forms are assigned or reserved
- how vendor or provisional terms are introduced safely

### Interoperability And Privacy-Semantics Risks If We Do Nothing

If the current shape is left mostly as-is, the likely problems are:

- different vendors will reuse the same short labels with different meanings
- declarations and policies will appear structurally compatible while not being
  semantically compatible
- unknown or extended terms will be handled inconsistently across devices and
  gateways
- privacy-relevant distinctions such as local processing, third-party transfer,
  retention, or derived-data handling will be hard to express without ad hoc
  per-vendor extensions
- the demo will look more standards-ready than the underlying semantics really
  are

### Habanero Follow-Up Implications

The protocol decision implies future demo and prototype follow-up work such as:

- add a scoped compact-term model rather than bare strings alone
- add declaration-side taxonomy binding, not just policy-side binding
- define and implement unknown-term validation behavior
- add a general rule-extension slot such as `constraints`
- move toward real declaration-to-policy matching semantics instead of relying
  only on device-specific override replacement
- remove or isolate prototype-only metadata fields that leak internal topology
  or placeholder authorization behavior

### What To Avoid In The Draft

- do not make raw IRIs the only participant-facing wire form
- do not leave compact terms unbound to stable identifiers
- do not let the demo JSON shape become the de facto semantic model unchanged
- do not postpone unknown-term behavior until after the protocol object model is
  fixed

### Cohesive Draft Story

The draft should tell the identifier story in this sequence:

1. participant-facing objects use a compact operational profile
2. taxonomy-bearing fields carry compact identifiers
3. core terms use reserved well-known prefixes and extension terms use explicit
   declared prefixes
4. each compact identifier maps to a stable namespace-based taxonomy term
5. taxonomy release metadata helps with validation and reproducibility
6. extensions and unknown terms are handled explicitly
7. the compact wire form stays readable for constrained devices and demos
   without sacrificing long-term interoperability

### Short Drafting Position

The shortest coherent statement of this decision is:

"The participant-facing protocol uses compact taxonomy term identifiers rather
than requiring raw IRIs in every message. Each compact identifier maps
deterministically to a stable namespace-based term identifier defined by the
taxonomy work. The protocol should reserve core prefixes and allow explicit
extension prefix declarations only where needed. The current Habanero JSON
demonstrates why compact terms are useful, but the protocol must add explicit
identifier binding, unknown-term handling, and extension rules so the compact
form remains interoperable."
