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
- every configured or discovered candidate origin MUST expose the registered
  `/.well-known/ppd` resource for metadata confirmation
- the returned Service Metadata Object identifies `service_base_uri`, which
  advertises the deployment's API mount point and versioned base path
- all operation references are resolved relative to `service_base_uri`; the
  protocol does not require the API to be mounted at a fixed origin-root path
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
- metadata confirmation through `GET /.well-known/ppd` on the candidate origin
  is mandatory
- participants use the advertised `service_base_uri` for protocol operations
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

Discovery mechanisms identify candidate service origins. The well-known
resource confirms PPD support and returns the participant-facing API base URI,
which may be mounted under a deployment-selected path prefix.

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
2. the device retrieves metadata from `GET /.well-known/ppd` on a candidate
   origin
3. the device validates the advertised service endpoint according to the
   applicable security profile
4. the device resolves the protocol's relative operation references against
   the advertised `service_base_uri`
5. only then does the device proceed into registration, declaration, policy
   retrieval, and acknowledgment

This keeps discovery link-neutral, preserves a narrow interoperable contract,
and avoids hard-coding one home-network topology or onboarding method into the
protocol baseline.

### Drafting Direction

Likely edits to the protocol draft:

- tighten the discovery section so it defines configured or provisioned
  endpoint support as the baseline
- use the registered `/.well-known/ppd` URI as the mandatory metadata
  confirmation step on each candidate origin
- advertise the versioned API base URI in metadata and resolve operation paths
  relative to it, allowing deployment-selected path prefixes
- classify automatic local discovery mechanisms as optional profiles unless a
  deployment profile requires them
- state explicitly that discovery yields candidates, while trust comes from the
  applicable security profile
- keep Wi-Fi-specific mechanisms as optional accelerators rather than baseline
  requirements

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline PPD discovery model is layered. Participants obtain candidate
service origins through configuration or optional discovery profiles, confirm
PPD support at the registered origin-level `/.well-known/ppd` URI, and use the
advertised `service_base_uri` for API operations. Additional local discovery
mechanisms are optional unless required by a deployment profile."

## 2026-10-13

### Origin-Level Bootstrap And API Base URI

The protocol no longer fixes the participant-facing API at `/ppd/v1` on the
origin root.
It uses the RFC 8615 well-known URI `/.well-known/ppd` as the root-level
metadata bootstrap. That metadata advertises a same-origin `service_base_uri`
whose path may contain a deployment-selected prefix and protocol version.
The operation paths are relative references resolved against that URI using
RFC 3986.

This resolves two different concerns at the proper layers:

- configuration and optional discovery profiles identify candidate origins;
- the well-known resource negotiates the API mount point for that origin.

The well-known URI does not discover the hostname or establish trust. The
existing discovery profiles still supply candidate origins, and the selected
service endpoint still has to pass the applicable authentication checks.
The protocol is intended for the Standards Track, so its IANA request uses
`IETF` as the change controller and `permanent` as the registration status,
consistent with RFC 8615. The architecture and taxonomy drafts remain
Informational.

This formal IANA role is distinct from CableLabs' internal maintenance
responsibility. Before publication, CableLabs should designate a named
technical owner to coordinate ongoing protocol maintenance: track issues and
errata, keep the draft and implementations aligned, and represent CableLabs in
standards discussions. That person is not the IANA change controller; the
registration's formal change controller is the IETF.

Working assumption: Daniel Smullen will serve as the interim CableLabs
technical owner, subject to confirmation with Brian Scriber. Revisit this
designation if responsibility moves to another CableLabs colleague or team.

The architecture draft should describe the same division of responsibility.
The taxonomy draft does not need an endpoint change because its scope is the
semantics and comparison of dataflow terms, independent of HTTP resource
addressing.
