# Association State Direction

This note tracks the working direction for the baseline association-state model
in the participant-facing protocol draft.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

Lift the existing Habanero association-state model into the baseline protocol
with only a narrow normative state vocabulary:

- `not_associated`
- `associated`
- `needs_reassociation`
- `stale_association`
- `broken`

These states are already implemented and exercised in the Habanero prototype
and are sufficient for baseline participant lifecycle interoperability.

The draft should not require the richer operator-surface and dashboard
enrichments that the demo uses around those states.

### Why This Direction Holds

- the prototype already has a real computed state model rather than ad hoc UI
  labels
- the current state set captures the baseline lifecycle distinctions the
  protocol actually needs
- lifting the same coarse model into the draft keeps the protocol close to the
  demo without importing all of the demo's operator affordances
- the remaining enrichments are useful for visibility and debugging, but they
  are not required to make baseline association work

### Baseline State Meanings

- `not_associated`:
  the participant has not yet completed the required delivery and receipt path
  for the current policy instance
- `associated`:
  the current effective policy instance has been delivered and acknowledged
  within the applicable freshness window
- `needs_reassociation`:
  a previously associated participant must repeat one or more lifecycle steps
  because the current policy instance or association validity basis changed
- `stale_association`:
  the participant previously had current association, but freshness expired
  without timely renewal
- `broken`:
  lifecycle records are contradictory, incomplete in a way that defeats
  trustworthy interpretation, or otherwise unusable as evidence of association

### What Should Stay Optional

The draft should treat the following as useful optional enrichments rather than
baseline protocol requirements:

- `required_lifecycle_step`
- human-readable `association_reasons`
- operator-facing summary counters and dashboard grouping
- network-observed or unmanaged visibility
- device-side or operator-side reset controls
- single-device attention ordering or other UI-specific presentation logic

These are valuable for operator visibility, debugging, and demo clarity, but
they are not strictly necessary for two interoperable implementations to manage
association state correctly.

### Why The Optional Boundary Matters

If the draft standardizes too much of the operator surface, it will:

- overfit to the Habanero dashboard model
- impose unnecessary UI and status-surface obligations on simpler
  implementations
- blur the line between baseline participant protocol behavior and local
  operator tooling

If the draft standardizes too little, it will:

- miss an already proven lifecycle model
- leave reassociation and staleness behavior underspecified
- force each implementation to invent incompatible association-state labels

The right cut is therefore:

- normative coarse states
- optional explanatory enrichments

### Relationship To Other Decisions

This direction is consistent with the earlier decisions that:

- acknowledgment is a receipt signal only
- current association means the current policy instance was received and
  acknowledged within freshness bounds
- conflict detection and resolution are separate from baseline acknowledgment
  and association state

### What To Avoid In The Draft

- do not invent a new association-state vocabulary when the prototype already
  has a workable one
- do not make dashboard-oriented enrichments mandatory for protocol conformance
- do not overload baseline association states with policy-compatibility or
  compliance semantics
- do not conflate network observation status with protocol association state

### Cohesive Draft Story

The draft should tell the association-state story in this sequence:

1. the participant completes registration, optional declaration, policy
   delivery, and receipt acknowledgment
2. the service computes one coarse association state for the participant
3. that state distinguishes current association, reassociation need, staleness,
   broken records, and lack of association
4. deployments may expose richer explanatory detail, but that detail is outside
   the baseline protocol requirement

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline protocol should standardize the coarse association states already
proven in the Habanero prototype: `not_associated`, `associated`,
`needs_reassociation`, `stale_association`, and `broken`. Richer fields such as
required next step, explanatory reasons, network-observation context, and
dashboard-specific grouping remain useful optional enrichments rather than
baseline interoperability requirements."
