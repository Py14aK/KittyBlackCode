---
name: sas-hash-fa
description: Use for SAS hash-object work on FA books — PD vintage lookup, account-key merge, URG migration counts, VoP match, S-matrix aggregation, MD5 chunked pass, and array-hash ports from Py14aK Hashigami. Triggers include hash merge macro, defineKey, Multidata Y, hash sort no dups, group sum with DoW, moving average hash, Horner multikey, path_finding_with_hash, and Black Belt Hashigami.
metadata:
  type: workflow
  version: "2026-09-17"
  source: Py14aK/Py14aK SaS Black Belt Hashigami plus Risk/path_finding_with_hash
  role: fa
---

# SAS Hash for FA

Port the pasted Hashigami patterns onto FA keys. Do not mix this skill with physics packs or personal-role packs. Load risk-analysis when the output is a PD table. Load this skill when the method is a hash object.

Canonical GitHub

- Py14aK/Py14aK folders SaS Black Belt Hashigami, SaS, Risk
- Grok-only notes live in Py14aK/KittyBlackCode/CoGro-
- FA product work lives in KittyBlackCode packs 01, 02, 11 and 2026-09-11-test

## When to use a hash

Use a hash instead of PROC SORT plus MERGE when the lookup table fits RAM, keys are account, month, URG, score band, or BENEF.IBAN, and you need one-pass aggregation, distinct counts, or last/first in an ordered iterator.

Do not use a hash as a PD model. It is a join and aggregation engine.

## FA key map

- Lookup find — APP/BEH account snapshot by account_id
- Multidata Y — multiple months or URG rows per account
- ordered A/D plus hiter next/prev — latest month, max default flag, min DPD
- HashSort plus ref — unique facility_key x month
- group sum / mean — S-matrix cell counts and observed default rate
- hash-of-hash distinct — unique counterparties per id
- moving average — 3-month rolling arrears or exposure
- MD5 of concatenated keys — compress wide composite keys
- WHERE chunk plus MD5_BYTE1 — RAM-safe pass over an unsorted book
- array hash plus prime hsize — hot-path lookup
- path_finding_with_hash — rebuild event chains from pid/id

Protected FA strings stay exact. Do not rename BENEF.ID, Default_12min, URG, MOB, PACS.004.
