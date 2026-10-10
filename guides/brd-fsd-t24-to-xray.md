# FSD section 5 is the Xray test

A use case in FSD section 5 is already a Jira Xray test case, written across the page. Transpose it and it is the test. Do not invent steps, and do not summarise the use case into a requirement sentence.

The CSV import rules stay in `guides/jira-xray-test-csv.md`. This page is only the transpose.

## Transpose

Section 5 is wide: one use case, steps sitting in columns (or one step per column of a sheet). Xray is tall: one step per row, same `TCID` on every row of that use case.

In Excel: copy the use-case block, Paste Special, Transpose. Each former column becomes one data row.

Then rename only the header so it matches the template they were given. The cells underneath keep the section 5 words.

| After the transpose | Xray column |
|---|---|
| Use case id | `TCID`, repeated on every step |
| Use case name | `Test Summary`, repeated on every step |
| What the FA does | `Action` |
| What the FA types | `Data` |
| What the screen must show | `Result` |

`Action` is the FA execution, in order, as a person at the screen would say it. "On the command line, type the command and press Enter." A sentence that starts with "The system shall" is not an Action. Put that sentence in `Result` if section 5 already has it there.

If section 5 does not state the expected screen text, `Result` is `GAP`. Do not write a likely message.

## DEV command rows, incoming and outgoing

A payment use case is not finished until both directions have a DEV command step. Those steps are part of the FA execution, not a note under the table.

Keep the command exactly as section 5 prints it, including the slash. The cell they named looks like this in the sheet:

```text
/tsbc CBPR.MNT
```

One row per direction:

| TCID | Test Summary | Action | Data | Result |
|---|---|---|---|---|
| the use case id | the use case name | On the command line, enter the outgoing DEV command and press Enter | `/tsbc CBPR.MNT` when that is the outgoing command printed in section 5 | The screen or message section 5 names, otherwise `GAP` |
| the same id | the same name | On the command line, enter the incoming DEV command and press Enter | The incoming command printed in section 5 | The screen or message section 5 names, otherwise `GAP` |

Put these two rows where section 5 places the send and the receive. If section 5 does not say where, put them after Validate.

If section 5 prints only one of the two commands, the other `Data` cell is `GAP`. Do not invent a second command, and do not copy `/tsbc CBPR.MNT` into both rows unless section 5 uses it for both.

## One Copilot turn

Attach section 5 for one use case, and the template header.

```text
Transpose this FSD section 5 use case into the Xray template. The use case is already the test.

Do not change the header.
Do not rewrite the step words. Action stays the FA execution from section 5.
One spreadsheet row per step. Repeat TCID and Test Summary on every row of this use case.
Data is what section 5 says to type. Result is what section 5 says the screen shows. If section 5 has no expected text, Result is GAP.
Add two rows that are not optional: the outgoing DEV command and the incoming DEV command.
Copy each command exactly. The outgoing example already printed is: /tsbc CBPR.MNT
If section 5 does not print the other command, Data for that row is GAP.
No code fence. No extra columns. Then stop.
```

Reject the answer if a step from section 5 is missing, if the command text was reworded, or if either DEV row is absent. Fix nothing in chat. Paste section 5 again with the same prompt.

## What this is not

BRD text does not become the steps. It can only supply the use case name when section 5 has a title that matches it. A T24 field token becomes `Data` only when section 5 already tells the FA to type that field.

One use case, one `TCID`. The next use case in section 5 is the next `TCID` in the same sheet.
