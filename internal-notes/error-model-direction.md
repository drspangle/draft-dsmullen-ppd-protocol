# Error Model Direction

This note tracks the working direction for structured protocol errors in the
participant-facing draft.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-12

### Decision

Keep the error model simple:

- use conventional HTTP status codes for the broad class of failure
- use `application/problem+json` as the structured error envelope
- define a small PPD-specific problem vocabulary for the protocol-specific
  reason

The draft should not invent a custom error envelope and should not try to make
HTTP status codes carry all PPD-specific meaning by themselves.

### Why This Direction Holds

- the current RESTful prototype already uses HTTP status codes for coarse
  failure classes
- HTTP status codes are good at broad transport and request-semantics
  distinctions, but not at the finer participant-lifecycle distinctions that
  PPD needs
- adding a small PPD problem vocabulary avoids stretching HTTP semantics
- using a standard problem envelope keeps the protocol readable and familiar
  without pulling in excessive new machinery

### Baseline Structure

The participant-facing draft should use the Problem Details model from
RFC 9457 as the baseline error object.

At minimum, error responses should carry:

- `type`
- `title`
- `status`
- `detail`

The draft may later define a very small number of optional extension members if
they are justified by concrete protocol needs.

### Minimal PPD Problem Vocabulary

The current working direction is to define only a small initial set of
protocol-specific problem types, such as:

- `invalid-request`
- `invalid-participant-binding`
- `reassociation-required`
- `stale-association`
- `policy-instance-mismatch`
- `unsupported-taxonomy-term`
- `term-resolution-failed`
- `policy-authority-unavailable`

Within that pair, the intended distinction is:

- `term-resolution-failed` when the service cannot deterministically expand the
  supplied compact identifier into a stable term identifier at all
- `unsupported-taxonomy-term` when deterministic expansion succeeds, but the
  resulting term is not supported for the relevant operation or deployment
  profile

These should be treated as protocol-specific reasons carried inside a standard
problem envelope, not as replacements for HTTP status codes.

### Baseline HTTP Mapping

The current working direction is to keep the HTTP mapping small and
conventional:

- `400` for malformed requests or missing required fields
- `401` for authentication failure
- `403` for authorization failure
- `404` for missing participant or policy state
- `409` for lifecycle or policy-instance state conflicts
- `422` for well-formed but semantically unprocessable content
- `503` for transient authority or service unavailability

This keeps the participant-facing semantics clear without overloading the HTTP
status space.

### Prototype Alignment Note

The current Habanero prototype already behaves broadly this way at the HTTP
layer, but it mostly returns plain-text error bodies rather than structured
problem documents.

One concrete prototype-versus-draft mismatch is that the gateway currently uses
`502 Bad Gateway` when the preference repository is unavailable behind the
gateway service.

For the participant-facing draft, we may want to normalize that situation to
`503 Service Unavailable` when the meaning to the participant is simply "the
PPD service cannot currently fulfill this request". That keeps the draft
participant-facing and avoids overexposing internal topology.

### What To Avoid In The Draft

- do not invent a custom PPD-only error envelope
- do not rely on plain-text response bodies as the normative protocol model
- do not force HTTP status codes to express all PPD-specific state by
  themselves
- do not define a large or highly granular problem vocabulary before concrete
  need exists
- do not let internal repository topology leak into the participant-facing
  error story more than necessary

### Cohesive Draft Story

The draft should tell the error story in this sequence:

1. use normal HTTP status codes for broad failure classes
2. use a standard structured problem envelope for machine-readable errors
3. define a small PPD-specific problem vocabulary for lifecycle and policy
   distinctions that HTTP status codes alone cannot express
4. keep extension members and subtype proliferation minimal unless later draft
   work demonstrates a real need

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline protocol uses conventional HTTP status codes for broad error
classes and `application/problem+json` for structured error responses. PPD
defines a small protocol-specific problem vocabulary for participant-lifecycle
and policy-specific failure reasons, rather than stretching HTTP status codes
or inventing a custom error envelope."
