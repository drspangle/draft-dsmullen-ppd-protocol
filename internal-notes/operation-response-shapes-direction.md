# Operation Response Shapes Direction

This note tracks the working direction for successful response bodies on the
baseline participant-facing operations.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as the remaining response-shape decisions are
closed out.

## 2026-05-14

### Why This Needs A Note

The current draft is stronger on request objects than on success-response
objects.

That is a likely reviewer criticism, because a protocol can appear precise on
the input side while still leaving too much room for divergence on the output
side.

The main response-shape questions are:

- what `POST /ppd/v1/device/register` returns on success
- what `POST /ppd/v1/device/declaration` returns on success when no comparison
  outcome is returned
- what `POST /ppd/v1/device/ack` returns on success

### Registration Result Decision

Current decision:

- successful registration should return a small explicit Registration Result
  Object
- that object should contain only the canonical `device_id`

Reasoning:

- the purpose of registration is to bind participant identity at the service
- returning only the canonical `device_id` makes that identity binding
  explicit
- repeating `service_uri` or other endpoint metadata would blur registration
  result semantics with metadata confirmation
- baseline registration is not trying to redirect the participant onto a
  different canonical endpoint

Shortest statement:

"Registration success should return a Registration Result Object containing the
canonical `device_id` and nothing else."

### Declaration Response Direction

Current direction:

- when a deployment chooses to expose declaration-to-policy comparison at the
  baseline participant-facing protocol boundary, it returns a Comparison
  Outcome Object on the declaration path
- that surface is diagnostic only
- it is not a bargaining channel, policy-relaxation mechanism, or homeowner-
  prompt path

Resolved direction:

- when declaration succeeds and the service does not return a comparison
  outcome, the successful response should use `204 No Content`
- when the service does return a comparison outcome, the successful response
  should use `200 OK` with a Comparison Outcome Object

Reasoning:

- declaration success does not need a second baseline result object when no
  additional interoperable payload is required
- `204 No Content` keeps the declaration path narrow and makes it harder for
  declaration success to accrete hidden negotiation semantics
- a returned Comparison Outcome Object remains explicitly diagnostic rather
  than a consent or bargaining surface

### Acknowledgment Response Direction

Current direction:

- acknowledgment success should return a small explicit Acknowledgment Result
  Object carrying resulting association state and renewed freshness data
- acknowledgment remains evidentiary only
- richer compatibility or compliance semantics remain out of scope for the
  baseline acknowledgment

### What To Avoid

- do not let operation success rely only on prose when the response body
  matters for interoperability
- do not duplicate metadata confirmation surfaces in registration responses
- do not let declaration success become a negotiation or consent channel
- do not overload acknowledgment success with compatibility or compliance
  meaning

### Short Position

The baseline response-shape story should stay narrow:

- registration returns canonical participant identity
- declaration returns `204 No Content` unless it optionally returns a
  diagnostic comparison outcome
- acknowledgment returns a small explicit result object carrying
  association-state and freshness information
- none of these operations should become a hidden negotiation surface
