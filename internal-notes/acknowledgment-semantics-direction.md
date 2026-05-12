# Acknowledgment Semantics Direction

This note tracks the working direction for what a baseline policy
acknowledgment means in the participant-facing protocol.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

The baseline acknowledgment is a receipt signal only.

It means, in substance:

- this participant received this specific policy instance
- the policy instance is identified by the bound `policy_id` and `policy_hash`
- the receipt occurred within the applicable freshness window

It does not mean:

- the participant agrees with the policy
- the participant can satisfy every rule in the policy
- the participant has proven compliance
- the participant has resolved all conflicts between household policy and any
  participant-originated policy material

### Why This Direction Holds

- it keeps the baseline lifecycle simple and implementable
- it avoids turning acknowledgment into an overloaded compatibility or
  compliance signal
- it lets the protocol establish current association without pretending the
  participant-side policy evaluation problem is already solved
- it keeps conflict handling and exception handling separate from the basic
  policy-receipt flow

### Relationship To Participant-Originated Policy Material

The participant may supply declaration material or other participant-originated
policy-related inputs, but that is a separate matter from acknowledgment.

The protocol should therefore treat these as different concerns:

- household or effective policy delivery
- participant declaration or participant-originated policy input
- conflict detection
- exception or override handling
- satisfiable versus unsatisfiable outcomes
- policy-instance acknowledgment

The baseline acknowledgment should not be used to collapse those concerns into a
single signal.

### Baseline Association Meaning

Under this direction, current association means:

- the participant is bound to the current policy instance for this association
  cycle
- the participant has received that policy instance
- the participant has acknowledged receipt of that specific instance within the
  required freshness window

Current association does not, by itself, establish that every policy rule is
understood, conflict-free, or technically satisfiable by the participant.

If the architecture later wants stronger participant-status signaling, that
should be defined as a separate mechanism rather than changing the meaning of
the baseline acknowledgment.

### Consequence For Term-Resolution Handling

This decision narrows the effect of unresolved taxonomy terms on
acknowledgment.

If the acknowledgment is receipt-only, then unresolved or disputed policy terms
are primarily a policy-processing and conflict-handling problem, not an
ack-validity problem.

The acknowledgment still must fail if:

- the referenced policy instance is not current
- the `policy_id` or `policy_hash` does not match
- freshness requirements are not met
- participant binding or replay protection fails

But the acknowledgment does not need to carry separate compliance semantics in
order to remain valid as a receipt.

### What To Avoid In The Draft

- do not describe acknowledgment as compliance proof
- do not imply that receipt means semantic agreement
- do not overload current association with stronger guarantees than the baseline
  protocol actually supports
- do not force conflict-resolution semantics into the acknowledgment operation

### Cohesive Draft Story

The draft should tell the acknowledgment story in this sequence:

1. the participant retrieves the current effective policy instance
2. the policy instance is identified by stable instance identifiers such as
   `policy_id` and `policy_hash`
3. the participant acknowledges receipt of that specific policy instance
4. the service uses that receipt, together with freshness and participant
   binding, to maintain current association
5. separate mechanisms may later define conflict handling, exceptions, or
   richer participant-status signaling

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline acknowledgment is a receipt for a specific policy instance, not a
claim of compliance or compatibility. Household-policy delivery, participant-
originated policy inputs, conflict handling, and exception handling remain
separate concerns. Current association therefore means the current policy
instance was received and acknowledged within the required freshness window,
not that every rule has been proven satisfiable by the participant."
