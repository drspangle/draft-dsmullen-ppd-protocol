# Discovery Profile Direction

This note tracks the working direction for the protocol draft's discovery
model.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-07

### Decision

Use a layered discovery profile.

The protocol draft should not require one universal automatic discovery
mechanism across all PPD-capable devices and deployments.

Instead:

- every participant MUST support a configured or provisioned PPD service
  endpoint
- every participant-facing PPD service endpoint MUST support
  `GET /ppd/v1/meta`
- every participant that learns a candidate endpoint through any discovery
  method MUST confirm that endpoint with `GET /ppd/v1/meta` before deeper
  interaction
- discovery yields candidate endpoints only
- trust in a selected endpoint comes from the applicable security profile, not
  from discovery alone

### Why This Direction Holds

- the draft is meant to cover broad classes of IoT devices rather than one
  hardware or onboarding model
- some devices can only handle a provisioned endpoint plus basic HTTP
- some devices can also support local DNS, mDNS or DNS-SD, DHCP hints,
  default-gateway probing, or onboarding-assisted discovery
- requiring all compliant devices to implement all of those mechanisms would
  raise complexity without creating a better interoperability floor
- requiring one specific automatic mechanism would overfit to a subset of home
  deployments and network topologies

### Interoperability Floor

The draft should create a real baseline rather than allowing discovery to
become completely optional or deployment-specific.

Minimum participant-facing baseline:

- configured or provisioned endpoint support is mandatory
- metadata confirmation through `GET /ppd/v1/meta` is mandatory
- candidate discovery remains separate from endpoint trust validation

This gives constrained devices a workable floor while still allowing richer
automatic discovery in deployments that can support it.

### Optional Discovery Profiles

The draft should leave room for optional automatic discovery profiles such as:

- local DNS name
- mDNS or DNS-SD
- DHCP-delivered endpoint hint
- default-gateway probing
- Wi-Fi onboarding hints such as DPP or setup-flow provisioning

A deployment profile may require one or more of these mechanisms, but the core
protocol draft should not assume that every compliant participant implements
all of them.

### Important Boundary

The discovery target is the participant-facing PPD service endpoint, typically
the gateway-facing `/ppd/v1` service.

The draft should not make clients discover the internal repository directly.
Internal gateway-to-repository topology should remain outside the baseline
client discovery contract.

### What To Avoid In The Draft

- do not make default-gateway probing the universal baseline
- do not imply that all compliant devices implement all discovery mechanisms
- do not let a layered profile collapse into a model where nothing
  interoperable is guaranteed
- do not blur candidate discovery with endpoint trust validation
- do not leak repository-internal deployment structure into participant-facing
  discovery language

### Cohesive Draft Story

The draft should tell the discovery story in this sequence:

1. a device obtains one or more candidate participant-facing service endpoints
   through provisioning or an optional discovery profile
2. the device confirms protocol support through `GET /ppd/v1/meta`
3. the device validates the selected endpoint according to the applicable
   security profile
4. only then does the device proceed into registration, declaration, policy
   retrieval, and acknowledgment

This keeps discovery link-neutral, preserves a narrow interoperable contract,
and avoids hard-coding one home-network topology or onboarding method into the
protocol baseline.

### Drafting Direction

Likely edits to the protocol draft:

- tighten the discovery section so it defines configured or provisioned
  endpoint support as the baseline
- make `GET /ppd/v1/meta` the mandatory confirmation step for discovered
  candidates
- classify automatic local discovery mechanisms as optional profiles unless a
  deployment profile requires them
- state explicitly that discovery yields candidates, while trust comes from the
  applicable security profile
- keep Wi-Fi-specific mechanisms as optional accelerators rather than baseline
  requirements

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline PPD discovery model is layered. All participants support a
configured or provisioned PPD service endpoint, and all candidate endpoints are
confirmed using `GET /ppd/v1/meta`. Additional local discovery mechanisms are
optional profiles unless required by a deployment profile."
