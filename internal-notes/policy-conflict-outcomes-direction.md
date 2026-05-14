# Policy Conflict Outcome Direction

This note tracks the working direction for how the protocol draft should treat
conflicts between household policy and participant-originated policy-related
inputs.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

The baseline protocol should define outcome categories only.

It should not standardize a conflict-resolution procedure.

The protocol may classify the result of comparing participant-originated
policy-related inputs against household policy or effective policy, but it
should not attempt to define:

- who is allowed to decide the resolution path
- what enforcement action the household prefers
- whether an exception should be granted
- which technical compromise should be chosen
- how a deployment should negotiate among multiple permissible options

### Why This Direction Holds

- the right resolution path depends on household intent
- households may want enforcement or exception behavior to be expressed in
  policy rather than hard-coded into the protocol
- the available flexibility depends on device capability and optionality
- the available flexibility also depends on technical and configurability
  limits on both sides
- a standardized resolution procedure would overfit to one governance model and
  one class of devices

### Boundary Between Protocol And Resolution Logic

The protocol should be able to carry or expose the coarse result of policy
comparison.

The protocol should not attempt to standardize:

- local user prompts
- household decision workflows
- vendor-specific remediation paths
- automatic fallback selection among device modes
- operator or backend exception-approval procedures

Those behaviors are deployment, policy-authority, or product-surface concerns,
not baseline participant-protocol concerns.

### Baseline Outcome Categories

The current working direction is to keep the baseline categories coarse and
operationally meaningful.

The minimum useful set is:

- `compatible`:
  participant-originated inputs do not conflict with the applicable household
  or effective policy
- `conditionally_satisfiable`:
  a conflict exists, but there is at least one permissible path such as a known
  exception, alternate mode, or constrained operating configuration
- `decision_required`:
  a conflict exists and cannot be resolved automatically by the baseline
  protocol; some off-protocol household, operator, or deployment decision is
  required
- `unsatisfiable`:
  the conflict cannot be satisfied within the technical or policy limits in
  view
- `indeterminate`:
  the comparison cannot be completed reliably, for example because necessary
  terms, mappings, or capability details are unavailable or unsupported

These categories are sufficient to let interoperable participants and services
talk about the state of the comparison without standardizing the resolution
workflow itself.

### Relationship To Acknowledgment

These categories are separate from the baseline policy acknowledgment.

The baseline acknowledgment remains a receipt for the effective policy
instance.

Conflict classification, exception handling, and satisfiability are separate
matters and should not be overloaded into the acknowledgment operation.

### Protocol Surface

The current direction is to expose these categories, when a deployment chooses
to expose them at all, on the declaration path rather than in policy retrieval
or acknowledgment.

That means:

- the declaration remains the participant-originated descriptive input
- the service may optionally return a structured comparison result after
  receiving that input
- the Effective Policy Object remains the household-originated normative object
- the Policy Acknowledgment Object remains a receipt for a specific policy
  instance

This keeps the comparison result attached to the operation that triggered it
without overloading the policy or acknowledgment objects with unrelated
semantics.

Important constraint:

- the declaration path is not a bargaining channel
- the baseline protocol should not let a participant request repeated
  comparison attempts, pressure the household for policy relaxation, or use
  the comparison surface to trigger homeowner consent prompting
- the service may expose a comparison result, but that does not create a
  participant entitlement to negotiation or to policy-element disclosure

### What To Avoid In The Draft

- do not define a universal conflict-resolution procedure
- do not assume the household always wants automatic denial or automatic
  exception
- do not bake one device-negotiation model into the baseline protocol
- do not let the declaration path become a policy-relaxation or consent-
  bullying channel
- do not collapse policy comparison outcomes into the receipt acknowledgment
- do not pretend every conflict can be resolved purely by protocol mechanics

### Cohesive Draft Story

The draft should tell the comparison story in this sequence:

1. the participant receives the effective household policy
2. the participant may also provide declaration or other participant-originated
   policy-related input
3. a deployment or policy authority may compare those inputs
4. when exposed at the baseline participant-facing protocol boundary, the
   result is carried as a declaration-path comparison outcome
5. that comparison surface is diagnostic only, not a bargaining or homeowner-
   prompt channel
6. the protocol does not standardize how the conflict is then resolved
7. household policy, device capability, and deployment logic determine the
   actual resolution path

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline protocol defines coarse outcome categories for conflicts between
household policy and participant-originated policy-related inputs, but it does
not define a universal conflict-resolution procedure. When a deployment
exposes such a result at the baseline participant-facing protocol boundary, it
should do so on the declaration path rather than overloading policy retrieval
or acknowledgment. That declaration-path surface is diagnostic only and should
not be turned into a participant-driven negotiation or homeowner-prompt
channel. Resolution depends on household intent, policy-defined enforcement or
exception behavior, device capability, and technical or configurability
limits. Acknowledgment of the current effective policy instance remains a
separate receipt signal."
