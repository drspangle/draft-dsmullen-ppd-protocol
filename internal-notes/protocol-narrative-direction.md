# Protocol Narrative Direction

This note tracks the working direction for the draft's top-level narrative,
actor language, and end-to-end protocol story.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` before more detailed object-level work.

## 2026-05-12

### Decision

The draft should tell a narrow end-to-end story about a home-side PPD service
and a device-side actor.

The baseline protocol is between:

- a home-side `PPD service endpoint`; and
- a device-side actor, formally the `PPD participant`, which is a device or a
  service acting on behalf of a device

The homeowner or household member is not the protocol-side participant in this
sense.

The draft should therefore tighten its narrative language so that:

- the human household side is the source of policy intent
- the home-side service endpoint exposes the participant-facing contract
- the device-side actor registers, optionally declares, retrieves policy, and
  acknowledges receipt

### Why This Direction Holds

- the term `participant` can be misread as including the homeowner or another
  human household actor
- the protocol itself is not between a homeowner and a device; it is between a
  home-side service and a device-side protocol actor
- the narrower wording makes the authority boundary and object semantics much
  clearer
- the rest of the draft reads more coherently once that actor split is made
  explicit up front

### End-To-End Story

The top-level draft narrative should be:

1. a device-side actor learns or is provisioned with a home-side PPD service
   endpoint
2. it confirms the endpoint and the applicable trust profile
3. it registers and may optionally describe itself
4. the home-side service returns the current effective household policy for
   that device-side actor
5. the device-side actor acknowledges receipt of that exact policy instance
6. both sides use freshness and lifecycle state to determine whether
   association remains current, stale, broken, or in need of reassociation

This narrative should also make clear what the protocol is not trying to do.

### Out-Of-Scope Functions That Should Stay Out Of The Opening Story

The opening sections should continue to say clearly that the baseline protocol
does not define:

- household policy authoring
- local dashboards or operator workflow
- internal repository or policy-authority protocols
- household-side enforcement decisions or remediation procedures
- participant-side compliance attestation beyond receipt acknowledgment

### Language Guidance For The Draft

The draft should continue to reuse the architecture term `PPD participant`, but
it should immediately clarify that this means a device or a device-side service
delegate, not a homeowner or household member.

Where helpful in narrative prose, the draft may use short clarifying phrases
such as:

- "device-side actor"
- "device-side participant"
- "home-side PPD service"

without replacing the normative architecture terms.

### Relationship To Earlier Decisions

This narrative direction is consistent with the earlier decisions that:

- declarations are descriptive
- effective policy is normative and household-originated
- acknowledgment is receipt only
- association is about current policy delivery plus fresh receipt
- conflict-resolution procedure remains out of scope

### What To Avoid In The Draft

- do not let the opening sections imply that the homeowner is the
  protocol-side `participant`
- do not blur home-side policy authority with device-side declaration
- do not let the introduction drift into operator dashboards, repository
  topology, or enforcement workflow
- do not describe acknowledgment as compliance or compatibility proof

### Short Drafting Position

The shortest coherent statement of this decision is:

"The draft's opening narrative should describe a participant-facing home-network
control protocol between a home-side PPD service endpoint and a device-side
actor. The formal term `PPD participant` still applies, but it should be
immediately clarified to mean a device or device-side delegate, not a homeowner
or other human household actor. The protocol's baseline job is to support
discovery, registration, optional declaration, effective-policy retrieval,
receipt acknowledgment, and freshness-bound association maintenance."
