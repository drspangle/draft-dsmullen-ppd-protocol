---
title: "Privacy Preference Declaration Protocol Specification"
abbrev: "PPDProt"
category: info

docname: draft-dsmullen-ppd-protocol-latest
number:
date:
consensus: false
v: 3
keyword:
 - privacy preferences
 - home networks
 - internet of things
 - device signaling
venue:
  github: "drspangle/draft-dsmullen-ppd-protocol"
  latest: "https://drspangle.github.io/draft-dsmullen-ppd-protocol/draft-dsmullen-ppd-protocol.html"

author:
 -
    fullname: "Daniel Smullen"
    organization: CableLabs
    email: "d.smullen@cablelabs.com"

 -
    fullname: "Brian Scriber"
    organization: CableLabs
    email: "brian.scriber@computer.org"

--- abstract

This document specifies a participant-facing protocol for Privacy Preference
Declarations (PPDs) in home networks.  The protocol is between a home-side PPD
service endpoint and a device-side actor, formally the `PPD participant`, which
is a device or a service acting on behalf of a device.  It defines baseline
operations for endpoint metadata confirmation, participant registration,
optional participant declaration, effective-policy retrieval, policy
acknowledgment, renewal, and reassociation.  This document complements the PPD
architecture and taxonomy documents by defining the message and sequencing
behavior needed for interoperable policy signaling.

--- middle

# Introduction

{{?I-D.draft-dsmullen-ppd-architecture}} defines the architectural roles,
trust boundaries, and lifecycle meaning for Privacy Preference Declarations
(PPDs) in home-network environments.
{{?I-D.draft-dsmullen-ppd-taxonomy}} defines the vocabulary used to express
privacy rules and participant declarations.
This document specifies the participant-facing protocol behavior that sits
between those two companion documents.

The protocol defined here is intentionally narrow.
It is designed to ensure that a device-side actor can discover or be
provisioned with candidate home-side PPD service endpoints, confirm the
selected endpoint, register, optionally describe itself, retrieve the current
effective household policy that applies to it, and provide a protected receipt
acknowledgment for that exact policy instance.
The protocol also defines how the home-side service and the device-side actor
keep association current over time, including renewal and reassociation
behavior.

In the formal architecture terminology reused here, the device-side actor is
the `PPD participant`.
That term can be easy to misread, so this document makes the intended boundary
explicit:
the protocol-side participant is a device or a service acting for a device, not
the homeowner, household member, or operator who set or review household
policy.

This protocol does not define local dashboards, operator workflow, household
policy authoring, device-behavior enforcement, or internal protocols between a
PPD service endpoint and a distinct policy authority.
Those functions can exist in deployments, but they are outside the baseline
interoperable contract defined here.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

This document reuses the terminology defined in
{{?I-D.draft-dsmullen-ppd-architecture}}.
In particular, it relies on the meanings of `PPD participant`,
`PPD service endpoint`, `policy authority`, `effective policy`,
`association`, `current association`, `stale association`, and
`needs reassociation`.

For clarity in this document, `PPD participant` always means a device or a
service acting on behalf of a device.
It does not refer to a homeowner, household member, or other human actor on
the household side of the system.

# Scope

This document specifies:

* the participant-facing transport and serialization baseline;
* metadata confirmation for discovered candidate service endpoints;
* the baseline operation set for participant registration, optional
  declaration, policy retrieval, policy acknowledgment, and renewal;
* message-object expectations for those operations;
* reassociation behavior when current association can no longer be confirmed;
  and
* protocol-visible error and security behavior.

This document does not specify:

* operator-only status, dashboard, or diagnostics surfaces;
* household policy authoring interfaces;
* internal service-to-authority protocols;
* automated enforcement behavior; or
* non-HTTP transport profiles.

# Protocol Model

## Roles

This protocol defines a participant-facing contract between:

* a home-side `PPD service endpoint`, which presents effective policy
  instances and records protected policy acknowledgments; and
* a device-side `PPD participant`, which is a device or backend service acting
  on behalf of a device.

A `policy authority` may exist behind the PPD service endpoint, but this
protocol does not require participants to discover or address that authority
directly.
When the service endpoint and policy authority are distinct, the deployment
MUST preserve the authenticity and integrity of the policy information presented
through the participant-facing endpoint.

The baseline end-to-end story is therefore:

1. the device-side participant learns or is provisioned with a home-side PPD
   service endpoint;
2. it confirms the endpoint and the applicable trust profile;
3. it registers and may optionally submit declaration data;
4. the home-side service endpoint returns the current effective policy for that
   participant;
5. the device-side participant acknowledges receipt of that exact policy
   instance; and
6. both sides use freshness and lifecycle state to determine whether
   association remains current or must be renewed or replayed.

## Transport and Serialization

The baseline participant-facing protocol uses:

* HTTP over IP;
* the path prefix `/ppd/v1`; and
* JSON request and response bodies using `application/json`.

This document treats JSON as the baseline interoperable encoding.
More compact encodings MAY be defined by future deployment profiles where
resource constraints justify them, but such profiles need to preserve the same
message semantics.

Deployments SHOULD protect participant-facing exchanges with transport security.
Where a deployment claims strong authenticated participation, it MUST provide a
way for the participant to authenticate the selected PPD service endpoint and
for the service endpoint to authenticate the participant identity used for
association and acknowledgment.

## Candidate Discovery and Metadata Confirmation

This protocol does not standardize a single discovery mechanism.
Participants MAY learn candidate PPD service endpoints through configured
provisioning, local naming, DHCP-delivered hints, multicast service discovery,
default-gateway probing, or comparable local-network mechanisms.
Discovery yields candidates only; it does not establish authority.

A participant that learns a candidate endpoint SHOULD confirm that the endpoint
supports this protocol before deeper interaction.
For that purpose, the baseline protocol defines:

* `GET /ppd/v1/meta`

The metadata response is expected to identify at least:

* the participant-facing service URI;
* the protocol version or profile identifier;
* the taxonomy version or versions understood by the service;
* whether participant declarations are supported;
* whether protected acknowledgments are supported; and
* the expected security mode or trust profile.

The metadata response MUST NOT expose household policy contents, participant
inventory, or acknowledgment history before the normal participant-facing trust
checks succeed.

# Participant Lifecycle

## Initial Association

The baseline participant lifecycle is:

1. obtain one or more candidate PPD service endpoints;
2. confirm a selected endpoint using `GET /ppd/v1/meta`;
3. authenticate the selected endpoint according to the deployment's trust
   profile;
4. register participant identity and metadata;
5. optionally submit a participant declaration;
6. retrieve the current applicable effective policy instance; and
7. acknowledge receipt of that specific policy instance.

Association is established only when the current applicable effective policy
instance has been delivered and acknowledged.
Acknowledgment is a receipt signal; it is not a claim of compatibility or
compliance.

## Renewal and Stale Association

Current association is freshness-bound.
A participant MUST renew association often enough that the PPD service endpoint
does not treat the participant as stale.
The participant-facing protocol therefore needs a way to communicate renewal
expectations.

The baseline effective-policy response and acknowledgment response MUST convey
one of the following:

* an absolute renewal deadline; or
* a bounded renewal interval from the time of response.

If the applicable effective policy instance remains unchanged but the
participant does not renew before the conveyed freshness limit, the participant
enters stale association.
The participant no longer has current association until it completes the
required renewal procedure.

## Reassociation Triggers

A participant enters `needs reassociation` when current association can no
longer be confirmed because:

* the applicable effective policy instance changed;
* participant state relevant to effective-policy derivation changed;
* enough state was lost that the previous association can no longer be trusted;
  or
* another invalidating event defined by the applicable deployment profile
  occurred.

When reassociation is required, the participant MUST retrieve and acknowledge
the current applicable effective policy instance again before current
association is restored.

## Non-Participating Devices

This protocol does not require every device on a home network to participate in
PPD.
Devices that do not participate remain outside the active message exchange.
Their presence may influence local management or enforcement decisions, but
such decisions are out of scope for this protocol.

# Protocol Operations

## Overview

The baseline participant-facing operation set is:

1. `GET /ppd/v1/meta`
2. `POST /ppd/v1/device/register`
3. `POST /ppd/v1/device/declaration` (optional)
4. `GET /ppd/v1/policy/effective/{device_id}`
5. `POST /ppd/v1/device/ack`

These operations form a narrow control path.
They let a device-side participant confirm the home-side service, identify
itself, optionally describe itself, retrieve the current effective household
policy that applies to it, and acknowledge receipt of that specific policy
instance.
They do not define household policy authoring, repository-facing workflows,
compliance attestation, or conflict-resolution procedure.

When the effective policy changes, when freshness expires, or when other
invalidating events occur, the same narrow operation set is replayed as needed
to restore current association.

A deployment MAY expose additional readback or manageability operations, but
those are not required for baseline interoperability.
This document also does not define internal repository-facing operations or
operator-only status endpoints.

## Metadata Confirmation

### `GET /ppd/v1/meta`

Purpose:

* confirm that a candidate endpoint supports the expected PPD protocol profile;
* advertise baseline feature support; and
* communicate security expectations before registration or policy retrieval.

A successful response SHOULD include:

* `service_uri`
* `protocol_version`
* `taxonomy_versions`
* `declaration_supported`
* `ack_supported`
* `security_mode`

## Registration

### `POST /ppd/v1/device/register`

Purpose:

* create or refresh the service endpoint's stored registration for a
  participant; and
* bind the participant's current protocol identity to the registration state.

The request body MUST include:

* `device_id`

The request body SHOULD include, when available and appropriate for the
deployment:

* `manufacturer`
* `model`
* `firmware_version`
* `hostname`

The following fields MAY be included when the deployment profile permits them:

* `mac_address`
* `ip_address`

A successful response SHOULD return the canonical `device_id` and any service
metadata the participant needs for later operations, such as the participant-
facing service URI.

## Declaration

### `POST /ppd/v1/device/declaration`

Purpose:

* provide optional participant-side declaration data that can inform effective
  policy derivation or later operator review.

Declarations are optional.
A participant that does not submit a declaration can still establish
association if it can retrieve and acknowledge the applicable policy instance.

The request body MUST include:

* `device_id`
* `declaration_id`

A declaration MAY include supported values for the taxonomy dimensions defined
in {{?I-D.draft-dsmullen-ppd-taxonomy}}, such as supported data types,
purposes, actions, sources, and destinations.

## Effective Policy Retrieval

### `GET /ppd/v1/policy/effective/{device_id}`

Purpose:

* return the effective policy instance currently applicable to the participant;
* return enough provenance information to identify what was acknowledged; and
* communicate the freshness limit for current association.

A successful response MUST include:

* `policy_id`
* `policy_hash`
* `taxonomy_version`
* `rules`
* either `renew_by` or `renewal_interval`

A successful response SHOULD include provenance fields that let later
inspection distinguish the household baseline from any more specific inputs,
such as:

* `base_policy_id`
* `override_policy_id` when a more specific policy layer was applied
* `computed_at`

This operation returns the policy instance the participant is expected to
acknowledge.
It is not required to expose the internal policy-authority topology or the
full derivation algorithm.

## Policy Acknowledgment

### `POST /ppd/v1/device/ack`

Purpose:

* record a protected acknowledgment that a participant received a specific
  policy instance.

The request body MUST include:

* `device_id`
* `policy_id`
* `policy_hash`

The acknowledgment payload is a receipt signal only.
It MUST NOT be interpreted as a claim that the participant can satisfy every
policy rule.
If deployments need richer participant-side compatibility or status reporting,
that behavior MUST be defined separately from the baseline acknowledgment.

A successful acknowledgment response SHOULD include:

* the resulting association state; and
* the next `renew_by` or `renewal_interval` value to be used for maintaining
  current association.

An acknowledgment that refers to a non-current or mismatched policy instance
MUST be rejected.

# Message Objects

## Service Metadata Object

The service metadata object describes a candidate endpoint before deeper
interaction.
It SHOULD include:

* `service_uri`
* `protocol_version`
* `taxonomy_versions`
* `declaration_supported`
* `ack_supported`
* `security_mode`

## Device Registration Object

The registration object identifies the participant and carries optional device
metadata.
The stable identifier is `device_id`.
Other metadata fields are deployment-dependent and do not replace the stable
participant identifier.

## Device Declaration Object

The declaration object carries participant-supplied capability or data-handling
information.
At minimum it contains `device_id` and `declaration_id`.
Additional fields SHOULD use the shared taxonomy dimensions defined in
{{?I-D.draft-dsmullen-ppd-taxonomy}}.

## Effective Policy Object

The effective policy object represents the policy instance the participant must
acknowledge.
It contains the policy identifier, hash, taxonomy version, rule set, and
freshness information.
It SHOULD also contain provenance fields that make later recordkeeping and
inspection meaningful.

## Policy Acknowledgment Object

The acknowledgment object binds a participant identifier to a specific policy
instance and policy hash.
Deployments that claim strong accountability properties MUST protect the
acknowledgment against forgery, replay, and stale-policy confusion.

## Error Object

Error responses SHOULD use a structured error object with at least:

* `code`
* `detail`

A deployment MAY include a hint about whether retry is appropriate.
Error responses MUST NOT leak more household or participant metadata than is
necessary to explain the failure.

# Error Handling

The baseline protocol uses conventional HTTP status codes.
At minimum, participants need to handle:

* `200 OK` for successful retrieval or update;
* `400 Bad Request` for invalid payloads or missing required fields;
* `401 Unauthorized` for failed authentication;
* `403 Forbidden` for authenticated participants that are not authorized for
  the requested operation;
* `404 Not Found` for missing participant or policy state;
* `409 Conflict` for conflicting participant identity state or acknowledgments
  that do not match the current policy instance; and
* `5xx` errors for transient service or policy-authority failures.

A participant that receives an error during renewal or reassociation MUST NOT
assume that it still has current association unless the service endpoint has
explicitly confirmed that state.

# Security Considerations

Candidate discovery and endpoint trust are separate concerns.
A participant MUST authenticate the selected PPD service endpoint according to
the deployment's security profile before treating policy information as
authoritative.

If a deployment claims authenticated participation, it MUST provide:

* participant authentication sufficient to bind registration and
  acknowledgment state to the same participant identity;
* policy integrity sufficient to identify the acknowledged policy instance
  unambiguously;
* freshness protection sufficient to prevent replay of old acknowledgments as
  evidence of current association; and
* protected storage or export of acknowledgment records when those records are
  used for later inspection or accountability.

When a PPD service endpoint fronts a distinct policy authority, the deployment
MUST preserve the authenticity and integrity of policy instances, policy hashes,
and freshness metadata across that internal boundary.
This document does not standardize the internal protocol used for that purpose.

The protocol SHOULD minimize metadata exposure during discovery, registration,
and policy retrieval.
In particular, discovery metadata and unauthenticated error responses SHOULD
avoid exposing household policy contents, participant inventories, or
acknowledgment history.
{{?RFC7258}} remains relevant to these design choices.

# Internationalization Considerations

Where policy tags, labels, or other string identifiers are exchanged in this
protocol, future profiles SHOULD define comparison and storage behavior that is
consistent across vendors and locales.
Where internationalized strings are used, alignment with {{?RFC7564}} SHOULD be
considered.

# IANA Considerations

This document has no IANA actions.

--- normative

--- informative
