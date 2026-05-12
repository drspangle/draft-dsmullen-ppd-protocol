# Declaration Shape Direction

Date: 2026-05-12

## Decision

- Keep the declaration object descriptive only.
- Replace flat `supported_*` capability arrays with a non-empty `statements`
  array of atomic descriptive cases.
- Keep combination semantics in the taxonomy work, while letting the protocol
  carry the specific combinations a participant is asserting.

## Why

Flat capability arrays are too lossy.
They force receivers either to assume an unintended cross-product of
dimensions or to push whole combinations into giant compound taxonomy terms.
Neither scales.

An atomic descriptive statement lets the participant say which combination of
taxonomy-defined dimensions actually applies without forcing the protocol draft
to enumerate all semantic combinations itself.

## Boundary

- The protocol draft defines the declaration container and the per-statement
  field shape.
- The taxonomy draft defines the meaning of the dimensions and how they
  compose.
- The protocol draft should not try to catalog all valid semantic
  combinations.

## Example Shape

Instead of:

- `supported_data_types`
- `supported_purposes`
- `supported_actions`
- `supported_sources`
- `supported_destinations`

the declaration should carry:

- `statements`: array of Declaration Statement Objects

where each statement is one descriptive case such as:

- `data_type`
- `purpose`
- `action`
- `source`
- `destination`
- optional `constraints`

## Drafting Position

The declaration object should require:

- `device_id`
- `declaration_id`
- `statements`

and optionally:

- `taxonomy`

Each declaration statement should mirror the same core dimensions used by
policy rules, but without a normative `effect`.
