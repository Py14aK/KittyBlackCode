# Hashigami patterns cleaned for FA

## 1. Lookup merge (single hit)

```sas
if 0 then set lookup(keep=account_id pd_hat urg);
if _n_=1 then do;
  declare hash h(dataset:"lookup(where=(base_sample=1))");
  h.defineKey("account_id");
  h.defineData("pd_hat","urg");
  h.defineDone();
end;
set book;
rc = h.find();
if rc ne 0 then call missing(pd_hat, urg);
drop rc;
```

## 2. Unique sort (HashSort + ref)

Keys `facility_key month`. Data holds GB_FLAG and score. `ref()` drops duplicate snapshots.

## 3. Latest / min in ordered set

`ordered:"D"` plus `hiter.next()` then `prev()` after a by-group load, then `h.clear()`. Use for latest month PD or minimum DPD in the vintage.

## 4. Group sum and distinct

One hash for SUM, one hash U keyed by (KEY, VAR) for UNQ. DoW over ID. Clear both hashes after each ID.

## 5. Mean imputation

Pass 1 stores n, s, m by id. Pass 2 replaces missing v with stored m. Do not impute the default flag.

## 6. MD5 chunked pass

```sas
MD5_BYTE1 = rank(char(md5(cats(of KN:, of KC:)), 1));
```

Loop `WHERE MD5_BYTE1 between lo and hi` for n_chunks of 4 or 10.

## 7. Path rebuild

From `Risk/path_finding_with_hash`. `h_path` keyed by observation id with pid. `h_next` inverts pid to nid. Walk to start, then follow nid. FA analogue is reconstructing a payment or arrears chain after a scramble of event rows.
