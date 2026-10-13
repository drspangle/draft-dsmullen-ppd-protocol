# Source Material

This note tracks the most relevant protocol-design artifacts in the related
gateway repository, typically checked out locally as
`../habanero-ppd-gateway`.

## Primary Inputs

- `design/ppd-api.md`
  - current gateway implementation's public `/ppd/v1` surface; this is
    implementation context, not a protocol requirement for a fixed API path
  - distinction between device-facing, operator-facing, and repository-facing
    APIs
- `design/protocol/ppd-protocol-spec.md`
  - local prototype protocol behavior, endpoint summaries, and lifecycle notes
- `design/ppd-client-requirements.md`
  - participant lifecycle expectations, renewal behavior, and reconnect cases
- `design/service-discovery-tradeoffs.md`
  - candidate discovery mechanisms, metadata confirmation, and trust boundary
- `design/ppd-security-pki.md`
  - staged security model, identity binding, and acknowledgement integrity
- `draft-notes/ppd-internet-draft-notes.md`
  - standards-facing summary of what should become architecture, taxonomy, and
    protocol-spec text

## Secondary Inputs

- `design/ppd-taxonomy.md`
  - local policy and rule-object shape
- `design/current-state.md`
  - implementation boundary between what exists now and what remains future work
- `design/preference-repository/README.md`
  - internal repository split and trust boundary context
