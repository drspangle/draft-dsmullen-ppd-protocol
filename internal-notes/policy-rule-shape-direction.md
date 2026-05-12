# Policy Rule Shape Direction

This note tracks the working direction for the baseline policy-rule object
shape and its boundary from participant-originated descriptive objects.

It is intended to support coherent edits to
`draft-dsmullen-ppd-protocol.md` as topic-by-topic decisions are made.

## 2026-05-12

### Decision

Keep the baseline rule model simple and explicitly scoped to the household-side
effective policy object.

The baseline rule shape is a constrained tuple with qualifiers:

- `data_type`
- `purpose`
- `action`
- `source`
- `destination`
- `effect`

That verdict field belongs only in a normative policy object sent by the
household-side PPD service or authority. It does not belong in baseline device
declarations.

### Descriptive Versus Normative Boundary

The protocol should keep these object families distinct:

- descriptive participant-originated objects:
  - registration
  - declaration
  - capability or constraint inputs
- normative household-originated objects:
  - effective policy
- evidentiary objects:
  - acknowledgment

Descriptive participant objects state what the participant is, supports, or may
do.

Normative policy objects state what the applicable household policy allows or
denies.

Acknowledgment objects record receipt of a specific policy instance.

### Why This Direction Holds

- it matches the actual participant-versus-household authority boundary
- it avoids letting device declarations masquerade as household policy
- it keeps the baseline declaration model simple and descriptive
- it gives the household-side effective policy a clear place to carry rule
  effects
- it leaves room for later participant-originated policy objects without
  polluting the baseline declaration object

### Rule Effect Field

The current Habanero examples use a `decision` field for the rule verdict.

The draft direction is to rename that field to `effect`, because that more
clearly communicates that the field belongs to a normative policy object rather
than to a descriptive participant object.

This field represents the effect of the rule when it matches. In substance, it
means:

- `allow`
- `deny`

The key semantic point is:

- declarations describe
- policies carry effects
- acknowledgments attest receipt

### Simple Baseline, Clear Extension Points

The baseline rule shape should remain simple.

The baseline rule tuple should use singular fields for its core dimensions.

When a policy needs to express multiple destinations, purposes, actions, or
other variations, the baseline model should represent that as multiple atomic
rules rather than array-valued core fields inside one rule.

The draft should avoid:

- a full dataflow graph model
- multi-layered embedded rule languages
- turning each core field into a mini-language
- array-valued baseline core dimensions that make single-rule semantics harder
  to interpret and compare

The draft should preserve explicit extension points such as:

- `constraints` for retention, locality, timing, transfer conditions, and
  similar rule refinements
- a namespaced extension container if later rule semantics need structured
  growth beyond the baseline tuple model

### Constraints Field

The baseline rule object should include an explicit optional `constraints`
field.

This field exists to preserve a stable place for rule qualifiers without
forcing the draft to standardize a large qualifier language immediately.

The baseline draft should therefore:

- define `constraints` as optional
- define it as a structured object, not a free-form string
- keep the initial standardized contents minimal
- allow the field to carry future standardized qualifiers as the policy
  semantics mature

### Initial Standardized Constraint Members

The current working direction is to standardize a very small initial constraint
set rather than leaving the field completely empty.

The best initial members are:

- `retention`
- `locality`

These are strong early candidates because they:

- are central to privacy semantics in home IoT
- are easy to explain to implementers and policy authors
- do not require a full negotiation or measurement framework to state
- are unlikely to be regretted as early baseline qualifiers

The draft should remain conservative beyond that.

Members such as transfer conditions, rate limits, or richer execution
conditions may be worth documenting in notes and examples, but they should not
be rushed into the first normative set unless there is a clear need.

### Constraint Examples

The draft and local notes should make room for simple examples, even if the
normative text stays concise.

For example, a rule might later appear in a shape such as:

```json
{
  "rule_id": "rule-001",
  "data_type": "ppd:temperatureReading",
  "purpose": "ppd:coreFunctionality",
  "action": "ppd:collection",
  "source": "ppd:sensor",
  "destination": "ppd:localProcessing",
  "effect": "allow",
  "constraints": {
    "retention": "ppd:ephemeral",
    "locality": "ppd:inHomeOnly"
  }
}
```

The exact term inventory remains taxonomy work, but examples like this help
keep the intended semantics understandable while the draft remains disciplined.

### Notes Versus Draft Detail

It is acceptable, and useful, to keep richer fleshing-out notes and additional
examples in the repository even when the Internet-Draft carries only a reduced
and concise normative form.

That lets the draft stay readable while still preserving:

- example shapes
- likely future qualifiers
- semantic cautions
- implementation follow-up ideas

### Why `constraints` Should Exist Now

Including the field now is preferable to deferring it because:

- it keeps the baseline rule model from becoming too flat
- it creates a clear place for later semantics such as retention, locality,
  transfer conditions, timing limits, and similar refinements
- it avoids forcing later drafts to change the top-level rule shape just to add
  qualifiers
- it preserves a simple baseline rule tuple while still leaving room for
  realistic privacy-policy growth

The intent is to reserve the structural slot now, not to overdesign the
contents immediately, while still standardizing the smallest clearly useful
initial members.

### Why Atomic Rules Are Better

The current working direction is to prefer many simple granular rules over
fewer compound rules with array-valued dimensions.

This holds because atomic rules:

- are easier to reason over
- are easier to compare for conflict detection
- are easier to explain in operator and household-facing tools
- avoid introducing set or cross-product semantics into the baseline rule model
- keep baseline implementations simpler

This also means that when conflicts need to be reported, the protocol can point
to a specific atomic rule rather than to one compound rule whose internal
combinations may be ambiguous.

### What To Avoid In The Draft

- do not put normative allow-or-deny semantics into baseline device
  declarations
- do not blur participant-originated description with household-originated
  policy
- do not overcomplicate the first rule model with graph-level flow semantics
- do not make baseline rule dimensions array-valued unless later evidence shows
  the atomic-rule model is insufficient
- do not close off future rule refinement by omitting an explicit `constraints`
  slot
- do not turn `constraints` into an unstructured catch-all text field

### Cohesive Draft Story

The draft should tell the rule-shape story in this sequence:

1. participants send descriptive registration and declaration objects
2. the PPD service returns an effective policy object for that participant
3. the effective policy contains normative rules with explicit rule effects
4. the participant acknowledges receipt of that specific effective policy
5. richer participant-originated policy material, if standardized later, is a
   separate object family rather than an extension of the baseline declaration

### Short Drafting Position

The shortest coherent statement of this decision is:

"The baseline declaration object is descriptive, not normative. The baseline
effective policy object carries normative rule effects such as allow or deny.
The baseline rule model remains a simple structured tuple with singular core
dimensions, one atomic rule per described case, and an explicit optional
`constraints` object for qualifiers and refinements. The initial standardized
constraint members should be minimal, with `retention` and `locality` as the
best early candidates. The normative rule verdict field should be named
`effect`, and it belongs only in the household-originated policy object."
