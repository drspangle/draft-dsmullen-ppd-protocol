# Security Profile Direction

This note tracks the working direction for the protocol draft's security
profiles and conformance floor.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

Use explicit security profiles.

The draft should not rely on generic security language alone. It should make
assurance differences normative and visible.

Top-level profile structure:

- authenticated direct-participation profiles defined by an accountability
  floor
- an authenticated backend-mediated extension profile

Within authenticated participation, the draft should leave room for a small set
of profiled mechanism families aligned to broad participant classes rather than
to arbitrary cryptographic choices.

Current direction:

- direct-device authenticated participation is baseline protocol scope
- backend-mediated authenticated participation remains in scope, but as an
  extension profile rather than as baseline behavior

### Why This Direction Holds

- the protocol needs a real path for constrained devices
- the protocol also needs a credible accountability story for registration,
  policy delivery, and acknowledgment
- generic wording alone leaves too much room for incompatible interpretations
- weakening participation until unauthenticated devices qualify would undercut
  the protocol's security purpose
- the high-assurance floor is not just too heavy for the first draft revision;
  it is too heavy as a general expectation for the full range of intended home
  devices

### Interoperability And Accountability Floor

The authenticated participation profile should require:

- the participant can authenticate the selected PPD service endpoint
- participant-facing exchanges are protected for confidentiality and integrity
- the service can authenticate the participant identity used for registration
  and acknowledgment
- the same participant identity is meaningfully bound across registration,
  policy retrieval, and acknowledgment
- the effective policy instance is uniquely identifiable, such as by
  `policy_id` plus `policy_hash` or an equivalent binding
- the acknowledgment is bound to that specific participant and that specific
  policy instance
- replay or stale-state protection prevents an old acknowledgment from being
  treated as evidence of current association
- authentication or integrity failure means the participant MUST NOT treat the
  resulting state as current association

This is an accountability floor, not a maximal-assurance floor.

The draft should not require as baseline:

- a specific mandatory mechanism such as mutual TLS
- signed policy objects in every deployment
- signed acknowledgments in every deployment
- manufacturer PKI or globally anchored device identity
- full enrollment lifecycle machinery, certificate revocation, or other
  heavier infrastructure assumptions across all home-IoT classes

### Why Not Pick One Mechanism Yet

Specificity is useful when it improves interoperable behavior.

The risk here is choosing a mechanism that hard-codes the wrong participant
model too early, for example:

- assuming every direct device can manage certificate lifecycle cleanly
- assuming every deployment has onboarding strong enough for one local-key
  model
- assuming backend-mediated ecosystems can be represented cleanly as ordinary
  direct-device participants

The draft should therefore be specific about required security properties and
profile boundaries before it becomes specific about one universal mechanism.

This is not an argument for staying generic forever. It is an argument for
being specific at the right layer first.

### Authenticated Participant Classes

The authenticated side should correspond to broad participant classes that
exist in home IoT:

- `constrained direct device profile`
- `certificate-capable direct device profile`
- `backend-mediated participant profile`

These are participant models, not merely cryptographic variants.

They let the protocol recognize durable ecosystem differences without pretending
that every participant can implement the same credential lifecycle.

### Baseline Versus Extension Scope

Current direction:

- baseline protocol scope should cover direct-device authenticated profiles
- backend-mediated participation should be treated as an extension profile

Reasoning:

- backend-mediated systems are real, but heterogeneous and harder to constrain
  coherently in a first baseline participant-facing protocol
- forcing a tight baseline model onto those systems may provoke resistance
  without improving the core protocol for direct home-IoT devices
- extension treatment gives those ecosystems room to define how they meet the
  core accountability properties without freezing the wrong delegation model
  too early

Important boundary:

- extension status does not mean lower accountability requirements
- it means the baseline protocol need not standardize the full backend-on-
  behalf-of-device interaction model in its first core profile set

### Extremely Constrained Devices

Extremely constrained devices still matter, but they should not redefine the
meaning of participation.

Current direction:

- all normative PPD participation is authenticated participation
- a direct participant that cannot authenticate itself meaningfully is not a
  conforming direct participant
- extremely constrained devices that cannot meet the minimum authenticated
  direct-participant bar should participate indirectly through a trusted
  intermediary, or remain non-participating

This preserves the protocol's core security purpose while still leaving room
to support low-end home-IoT ecosystems through gateways, hubs, or comparable
controllers.

### What To Avoid In The Draft

- do not hide materially different security outcomes behind generic wording
- do not make plain HTTP or similarly weak local testing modes look like the
  normal interoperable baseline
- do not require one mechanism across all participant classes before the
  participant model is stable enough to justify it
- do not let backend-mediated systems distort the baseline direct-device
  profile
- do not treat extension profiles as exempt from the core accountability
  properties

### Cohesive Draft Story

The draft should tell the security story in this sequence:

1. participant-facing security is profile-based rather than monolithic
2. all normative participation is authenticated participation
3. authenticated participation is defined by a clear accountability floor
4. authenticated participation can be realized by a small set of participant-
   class-aligned profiles
5. direct-device profiles are baseline
6. extremely constrained devices that cannot meet that bar are indirect or
   non-participating
7. backend-mediated participation is an extension profile that still has to
   satisfy the same core accountability properties

This keeps the draft specific where interoperability depends on specificity,
while avoiding an overly narrow credential assumption for the home-IoT space.

### Drafting Direction

Likely edits to the protocol draft:

- define explicit top-level security profiles instead of relying on generic
  trust language alone
- use concise profile identifiers and metadata naming that make authenticated
  participation the baseline assumption rather than repeating `auth-` on every
  profile value
- describe the accountability floor for authenticated participation as a set of
  required properties
- scope baseline protocol text around direct-device authenticated profiles
- state clearly that no unauthenticated direct-participation profile exists
- direct extremely constrained devices toward trusted-intermediary
  participation instead of weakening the direct profile
- reserve backend-mediated participation for an extension profile that must
  still satisfy the same core security properties
- defer selection of one universal mechanism until the participant-profile
  model is mature enough to justify it, or choose a very small profiled set
  instead of a single mandatory mechanism

### Short Drafting Position

The shortest coherent statement of this decision is:

"The protocol defines explicit authenticated security profiles.
Authenticated participation is defined by endpoint authentication, participant
authentication, policy-instance integrity, and freshness protection sufficient
to make current association and acknowledgment meaningful. Baseline protocol
scope covers direct-device authenticated participation, while backend-mediated
participation is treated as an extension profile that must still satisfy the
same core accountability properties. Extremely constrained devices that cannot
meet the minimum authenticated direct-participant bar are expected to
participate indirectly or remain non-participating."
