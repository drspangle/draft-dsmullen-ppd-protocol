# Trusted Intermediary Examples

This note makes the "trusted intermediary" model more concrete for discussion
and review.

It is not intended to force draft text to enumerate product classes, but to
prepare a coherent answer if reviewers argue that the protocol does not say
what should happen for extremely constrained devices.

## 2026-05-13

### Purpose

The protocol direction now assumes:

- all normative PPD participation is authenticated participation
- extremely constrained devices that cannot meet the minimum authenticated
  direct-participant bar should participate indirectly through a trusted
  intermediary, or remain non-participating

The predictable criticism is:

"What is this intermediary supposed to be in a real home-IoT deployment?"

This note answers that question concretely without pushing product examples
into the Internet-Draft itself.

### Core Model

A trusted intermediary is the component that actually acts as the PPD
participant on behalf of one or more subordinate devices that cannot implement
the baseline authenticated direct-participant contract themselves.

That intermediary is responsible for:

- authenticating to the home-side PPD service
- authenticating the home-side PPD service before trusting policy material
- carrying participant-facing confidentiality and integrity protection
- submitting declarations or other descriptive statements on behalf of the
  subordinate device when applicable
- retrieving effective policy and acknowledging the exact policy instance that
  applies

This is not a loophole for weakening the protocol. It relocates the
participant boundary to a component that can actually satisfy the protocol's
security and lifecycle requirements.

### Concrete Intermediary Classes

These are the most plausible classes of trusted intermediary for extremely
constrained devices in home-IoT deployments.

#### Local multi-protocol hub or bridge

Examples in kind:

- Zigbee bridge
- Z-Wave controller
- Bluetooth Low Energy accessory bridge
- Thread border router or comparable home-automation bridge

Why this fits:

- the subordinate devices already depend on the bridge for network
  reachability, onboarding, orchestration, or translation
- the bridge is usually the component with the richer IP stack, persistent
  storage, and credential management needed for authenticated PPD
  participation

#### Vendor hub, base station, or appliance controller

Examples in kind:

- camera base station
- alarm panel
- thermostat controller
- smart-lighting hub
- lock or access-control gateway

Why this fits:

- many home devices already ship as accessories of a vendor-managed local hub
- the hub often aggregates policy-relevant device behavior and exposes the
  household-facing control surface
- the hub is a natural place to speak PPD for devices that are otherwise too
  limited

#### Household automation controller

Examples in kind:

- a dedicated home-automation controller
- a local smart-home server
- an ISP- or operator-managed home gateway with explicit device-management
  responsibilities

Why this fits:

- these systems often already maintain inventory, capability information, and
  household automation state
- they can serve as a local policy mediation point when they have a real trust
  relationship with the subordinate device

#### Backend service acting through a trusted local anchor

Examples in kind:

- a vendor cloud service that is cryptographically and operationally bound to
  a local hub or gateway
- a managed service that represents a subordinate device identity only because
  a trusted local controller delegated that role

Why this fits:

- some ecosystems already centralize device identity and lifecycle state in a
  vendor service
- the protocol already leaves room for a backend-mediated extension profile

Important limit:

- this is weaker as a baseline assumption than a local hub or bridge
- it should not become a generic excuse for unbound cloud-only assertions

### What Should Not Count

These do not automatically qualify as trusted intermediaries.

#### Generic IP router or switch

A normal home router, AP, or switch is not enough merely because traffic
passes through it.

Why not:

- transit visibility alone does not establish a trustworthy device-specific
  identity relationship
- a generic forwarding device usually does not have the declarative or
  lifecycle knowledge needed to speak on behalf of the subordinate device

#### Passive network monitor

A service that only observes traffic is not a trusted intermediary in the PPD
sense.

Why not:

- observation is not representation
- the protocol requires authenticated participant behavior, not just external
  inference

#### Ad hoc mobile app proxy

A smartphone app that happens to configure a device should not automatically be
treated as the participant.

Why not:

- setup tooling is not the same thing as a stable trusted control point
- the app may not have durable authority or lifecycle state after onboarding

#### Unbound cloud relay

A cloud service that cannot show a trustworthy binding to the subordinate
device should not qualify.

Why not:

- otherwise the architecture collapses back into anonymous or weakly bound
  claims about what a device is and does

### Criticism Response

If reviewers ask whether this model is too hand-wavy, the strongest answer is:

- this is not an invented escape hatch
- home-IoT deployments already rely heavily on hubs, bridges, border routers,
  base stations, and controllers to represent low-end devices
- the protocol is formalizing where the participant boundary should sit when
  the subordinate device cannot meet the authenticated direct-participant bar

The protocol is therefore not demanding that every battery sensor, lock
accessory, or radio endpoint independently implement the full authenticated
PPD stack. It is requiring that the component which does participate directly
be one that can actually carry the security and lifecycle obligations.

### Important Future Semantics

The intermediary model raises follow-on questions that the baseline protocol
does not need to solve immediately, but which are worth tracking:

- how the intermediary identifies the specific subordinate device on whose
  behalf it is speaking
- whether the protocol later needs a richer provenance model that distinguishes
  direct-device declarations and acknowledgments from intermediary-originated
  ones
- how one intermediary safely represents multiple subordinate devices without
  collapsing them into one coarse identity

These are real design questions, but they are not reasons to weaken the
baseline participation requirement.

### Short Position

If this criticism appears, the concise response should be:

"For extremely constrained devices, the expected participant is not the tiny
endpoint itself but a trusted local hub, bridge, base station, controller, or
other intermediary that already manages that device and can satisfy the
authenticated PPD lifecycle on its behalf. Generic transit devices, passive
observers, and unbound cloud relays do not qualify."
