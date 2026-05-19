# Taxonomy Coordination Follow-Ups

This note records protocol-draft follow-ups that are likely once the taxonomy
draft settles the next round of semantic design decisions.

## Why This Matters

The protocol draft already assumes:

- declarations carry atomic descriptive statements;
- effective policy carries atomic normative rules;
- both use the same core dimensions; and
- both can carry a shared structured qualifier object currently named
  `constraints`.

That makes the protocol draft tightly coupled to the taxonomy model, even when
the protocol remains intentionally agnostic about the full taxonomy semantics.

## Current Protocol Surfaces Likely to Change

### 1. `Constraints Object` Terminology

The protocol currently defines a wire object named `Constraints Object`.

Taxonomy-side discussion now treats this concept more precisely as dataflow
qualifiers rather than rule modality.

Open protocol coordination question:

- keep the wire field named `constraints` for stability, while clarifying in
  prose that the members are dataflow qualifiers; or
- rename the wire object and field later if the semantic mismatch becomes too
  costly.

Current bias:

- do not rename lightly; prefer conceptual clarification first.

### 2. Initial Qualifier Members

The protocol currently hard-codes:

- `retention`
- `locality`

as the initial standardized members.

Taxonomy work now suggests:

- retention may need stronger semantics, including categorical poles such as
  `ephemeral` and `indefinite` plus explicit quantitative refinement for
  bounded cases; and
- `locality` is probably not the right long-term name for the second qualifier
  family.

### 3. Example Drift

The current declaration and policy examples use:

- `ppd:shortLived`
- `ppd:householdApprovedRemoteService`

Those examples may need revision if the taxonomy moves away from a fuzzy
retention-class ladder and reframes the current locality/trust-boundary family.

### 4. Comparison Framing

The protocol already defines coarse comparison outcomes, but the draft could
more clearly state that the compared units are atomic privacy-relevant
dataflows expressed as declaration statements and policy rules.

That clarification belongs in the protocol once the taxonomy model is stable
enough to anchor it.

## Current Coordination Rules

- Let taxonomy settle the semantic model first.
- Update protocol internal notes before editing protocol draft prose.
- Keep the protocol responsible for message shape and carrying rules, while the
  taxonomy remains responsible for the meaning and comparison semantics of the
  role-fillers and qualifiers.
