# Runtime Conflict Signaling Direction

This note captures the current intended direction for runtime conflict
signaling in the participant-facing protocol draft.

It is intentionally narrower than the broader declaration-path comparison
story in `policy-conflict-outcomes-direction.md`.

## 2026-05-29

### Current Direction

The draft should keep three things distinct:

1. baseline policy acknowledgment;
2. baseline association state; and
3. optional runtime conflict signaling.

The current intended architecture is:

- a participant may acknowledge the current effective policy instance and
  remain currently associated;
- that same participant may also separately signal that its present runtime
  behavior conflicts with the acknowledged policy instance; and
- any remediation beyond surfacing that signal is deployment-specific.

### What This Means For The Draft

The protocol draft already says:

- acknowledgment is receipt-only;
- richer participant-side status reporting must be defined separately from the
  baseline acknowledgment; and
- the baseline association-state vocabulary is limited to
  `not_associated`, `associated`, `needs_reassociation`,
  `stale_association`, and `broken`.

That direction should be made explicit enough that implementers do not infer
that:

- runtime conflict becomes a new baseline association state; or
- a fresh acknowledgment resolves runtime conflict by itself.

### Intended Runtime-Conflict Semantics

The intended model is:

- `associated` still means the current policy instance was delivered and
  acknowledged within freshness bounds;
- runtime conflict is an orthogonal condition that can coexist with current
  association; and
- the conflict signal exists to inform the household or operator that the
  participant reports behavior that does not match the acknowledged policy.

That signal does not, by itself:

- disassociate the participant;
- force policy redelivery;
- invalidate the acknowledgment record; or
- mandate one specific remediation path.

### Relationship To Declaration-Path Comparison Outcomes

Declaration-path comparison outcomes and runtime conflict signaling should stay
separate.

The declaration path remains the right place for coarse results such as:

- `compatible`
- `conditionally_satisfiable`
- `decision_required`
- `unsatisfiable`
- `indeterminate`

Those categories describe comparison between participant-originated inputs and
household policy at the declaration boundary.

Runtime conflict signaling is different:

- it is post-association;
- it reflects current participant-reported behavior against the acknowledged
  policy instance; and
- it may be surfaced through an optional status-reporting extension rather than
  through the declaration response.

### Draft Follow-Up To Capture

The protocol draft should add one short explicit clarification that:

- optional participant-side runtime conflict signaling may coexist with current
  association;
- such signaling is separate from baseline acknowledgment semantics; and
- any resulting remediation, control, or enforcement behavior remains out of
  scope for the baseline participant-facing protocol.
