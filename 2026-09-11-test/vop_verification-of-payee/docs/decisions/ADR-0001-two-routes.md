# ADR-0001: the enquiry offers two routes, not one

Date: 2026-09-09
Status: proposed — awaiting team confirmation

## Context

The enquiry exposes two actions on the same rows. Early in the discussion they
were treated as variants of one action, which produced the question of whether
regenerating a request should overwrite the existing record.

## Decision

They are two routes with different relationships to identity.

- *Generate request* always creates a new record with a new id, whether it is
  invoked from the last row or from an existing row without an FT. The source
  row is never overwritten.
- *Create FT* always operates on the selected existing request, reads it by its
  own id, and refuses if that record already carries an FT reference.

## Consequences

- A completed row stays visible and is not a dead entry (R02).
- Exactly one last row is always present (R03, R04).
- The duplicate-FT guard must live where the FT is created, not in the render
  path — a stale view must not be able to bypass it (AC08, V09).
- The identifier scheme becomes load-bearing, which makes V01 the first
  blocking decision rather than a naming detail.

## Superseded reasoning

An earlier reading recommended that regenerating from an existing row reuse the
same record. The second transcript excerpt describes the fourth and fifth rows
producing the same outcome — new requests with different ids. That reading is
withdrawn and kept here as history.
