# Taxonomy Binding Direction

This note tracks the working direction for how the protocol draft should bind
message structure to an extensible taxonomy.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

The protocol should be rigid about message structure and flexible about
taxonomy vocabulary.

The primary semantic hook should be the taxonomy term identifier itself, not a
protocol-level taxonomy version string by itself.

Version or release metadata should remain important for validation,
reproducibility, caching, and debugging, but it should not be the only thing
that tells an implementation what a term means.

### Why This Direction Holds

- the protocol needs a stable wire skeleton for interoperable messages
- the taxonomy needs broad buy-in and room for later extension
- closed protocol enums would freeze the vocabulary too early
- relying on a single `taxonomy_version` field as the main semantic hook is too
  coarse for ontology- and namespace-oriented extension models
- extensible vocabulary systems such as OWL-style ontologies and W3C DPV use
  stable identifiers and namespaces for terms, with release or version metadata
  as a secondary mechanism

### Protocol Versus Taxonomy Boundary

The protocol draft should define:

- object shapes
- field names
- field types
- required versus optional fields
- where taxonomy-bearing fields appear
- how implementations handle unknown or unsupported terms
- how extensions are encoded

The taxonomy work should define:

- the actual term space for data types, purposes, actions, sources, and
  destinations
- relationships among those terms
- extension rules
- deprecation policy
- contribution and review path for adding new terms

Shortest summary:

- the protocol standardizes the container
- the taxonomy standardizes the vocabulary

### Primary Semantic Hook

Current direction:

- taxonomy-bearing fields should carry stable taxonomy term identifiers
- those identifiers may be represented in a compact syntax or an IRI-derived
  form, but the term identifier is the primary meaning hook
- vocabulary release metadata may be carried alongside the object so an
  implementation knows which published vocabulary release or validation target
  was in view when the object was produced

This means the draft should not treat `taxonomy_version` as the only field that
defines meaning.

### Habanero Demo Relevance

The current Habanero demo is useful guidance because it already shows the kind
of lightweight JSON shape that is plausible for constrained or demo-friendly
participants.

Current prototype observations:

- policy examples use simple string-valued taxonomy fields such as
  `data_type`, `purpose`, `action`, `source`, and `destination`
- declarations use arrays of simple strings such as `supported_data_types`,
  `supported_purposes`, `supported_actions`, and `supported_destinations`
- policy objects currently include a policy-level `taxonomy_version` string
  such as `draft-dsmullen-ppd-taxonomy-02`

That current shape is:

- easy to read in demo JSON
- easy for simple clients to generate
- easy for the dashboard and policy viewer to explain

But it is also semantically thin if the draft stops there, because a bare
string without a stable identifier or namespace story does not scale well to
cross-vendor extension.

### Implication For The Next Wire-Format Decision

The current demo argues against a design that forces every participant-facing
message to use long raw IRIs everywhere as the only permitted surface form.

It also argues against leaving term strings entirely unscoped.

The next decision should therefore ask:

- should the protocol carry raw IRIs directly in taxonomy-bearing fields
- or should it allow compact identifiers, with a clear mapping to stable
  namespace-based identifiers

The current Habanero JSON strongly suggests that some compact surface form is
worth preserving so the protocol remains readable and close to what a real demo
or constrained client can emit.

### What To Avoid In The Draft

- do not hard-code closed enums for all taxonomy dimensions
- do not make a single version string the sole semantic hook
- do not leave taxonomy-bearing strings entirely unscoped
- do not force a wire form that is so heavy that it diverges sharply from the
  lightweight participant JSON the demo is trying to model
- do not let protocol-schema simplicity prevent later shared extension of the
  taxonomy

### Cohesive Draft Story

The draft should tell the taxonomy story in this sequence:

1. protocol objects carry taxonomy-bearing fields in a stable typed structure
2. the meaning of those fields comes from stable taxonomy term identifiers
3. taxonomy release metadata can be carried for validation and reproducibility
4. the taxonomy itself can evolve through reviewed extensions without changing
   the core protocol object model
5. participant-facing JSON should remain practical for constrained devices and
   demos, even while the underlying taxonomy remains extensible

This keeps the protocol concrete without freezing the vocabulary too early.

### Drafting Direction

Likely edits to the protocol draft:

- describe taxonomy-bearing fields as carrying term identifiers rather than
  closed enumerated values
- treat taxonomy release metadata as secondary validation context rather than
  the sole semantic key
- when service metadata advertises taxonomy support, name that surface in terms
  of supported taxonomy releases rather than generic taxonomy versions
- define unknown-term and extension behavior explicitly
- keep the message schema stable even as the vocabulary grows
- choose a wire-level term-identifier strategy that stays reasonably close to
  the current Habanero demo JSON

### Open Next Decision

The next question to decide is:

- raw IRI-only taxonomy term encoding
- compact identifiers with a defined mapping to stable namespace-based term
  identifiers

The current demo suggests that compact identifiers deserve strong consideration.
