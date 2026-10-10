# The Xray test is the bench we ran

Section 5 already has the use case. Do not copy it, and do not transpose it into Jira.

The test is the execution of the bench that was built and run. The rows are in `guides/xray-bench-execution.csv`. Import that file with the rules in `guides/jira-xray-test-csv.md`.

Three tests:

| TCID | What the FA does | Result already seen |
|---|---|---|
| BENCH-01 | `ENQ TXN.ENTRY`, id `FT000`, date `20261009`, Run enquiry | Banner is No such customer |
| BENCH-02 | Same enquiry with `FT2610090001` / `20261009`, then `Иван` in `Ben.name.client`, Validate | `Ben.name.client` is the row under IBAN. Banner is Checked. Empty name blocks. A Latin name warns. |
| BENCH-03 | `FT,UBB.OUT.EUR.PMNT.BR NEW`, payer First, one amount, Validate, Accept warning | Credit account shows VOSTRO. Both amounts are rejected. One amount raises Warning: Customer sector mismatch. |

BENCH-03 ends with the two DEV command steps, outgoing then incoming. The command typed on the bench is `/tsbc CBPR.MNT`. The bench answers `Unknown command` for both. That is the result of this build. It is not a second copy of a section 5 use case.
