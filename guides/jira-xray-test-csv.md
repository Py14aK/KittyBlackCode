# Jira test cases from the CSV template

Hand this to the team that is failing Copilot CSV generation. The work is filling a template. It is not asking a chat to invent a spreadsheet.

Source for the importer rules: [Xray — Importing Manual Tests using Test Case Importer](https://docs.getxray.app/display/XRAY/Importing+Manual+Tests+using+Test+Case+Importer). Checked 2026-10-10. This is the Server/Data Center importer (Tests menu → Test Case Importer, or System → External System Import → Xray Test Case Importer). It is not the plain Jira CSV importer.

## What the template already is

The header row is the contract.

- Keep every header cell. Same spelling, same order.
- Fill cells under that header.
- Do not add a column because it sounds useful.
- Do not rename `TCID` to `Test id`, or `Test Summary` to `Title`.

You may name columns anything only when you are ready to map them by hand on the Field Mapping page. A file that does not match the template they were given will not reuse a saved mapping.

The Server template header, taken from Xray’s own example file, is this line and no other:

```text
TCID;Test Summary;Test Priority;Component;Action;Data;Result
```

The separator is a semicolon. The importer map for that header is fixed:

| CSV column | Jira / Xray field |
|---|---|
| TCID | Test Case Identifier |
| Test Summary | summary |
| Test Priority | priority |
| Component | components |
| Action | Action |
| Data | Data |
| Result | Expected Result |

`Result` is the column name. `Expected Result` is the field it maps to. A file that says `Expected Result` in the header does not match this template. Issue fields are filled on the first row of a test only. Later step rows leave Test Summary, Test Priority, and Component empty.

## What the template does not contain

The CSV does not carry the project setup. A perfect file still fails when any of these is missing:

- The project has the Xray issue type **Test**, and the Test screens include the fields you map.
- The person importing has **Bulk Change** and **Create Issues** on that project.
- Every value you write already exists in Jira: priority name, component, label rules, user name, select-list option. Unknown priority does not stop the import. Xray stores the default priority, or the lowest one.
- A field that is required on the Test create screen, and is not a column in the file, still blocks creation. The template cannot list that field. Look at the create screen, not at the CSV.
- The delimiter in the file matches the delimiter typed on the Setup page. Comma file plus semicolon setting, or the reverse, is a failed import.
- Encoding is the encoding selected on the Setup page. For Cyrillic or other non-ASCII text, use UTF-8 on both sides.

## Why Copilot "cannot create the CSV"

Asking Copilot to create a CSV throws away the template.

Copilot then does the things the importer rejects:

- One row per test, with the steps numbered inside a single cell. The importer wants one row per step.
- New headers.
- A markdown table, or a code fence, which is not a file.
- Smart quotes, or a comma inside a field that is not wrapped in straight double quotes.
- A file cut off because the chat ran out of length.

Excel is the right place. Copilot only fills cells.

## The row rule

One test is many rows. Rows of the same test share one `TCID`.

Repeat `TCID` and `Test Summary` on every step row. Do not leave them blank on step 2 and hope the importer remembers step 1.

```csv
TCID,Test Summary,Action,Data,Result
T1,Unknown enquiry stays closed,Open ENQ TXN.ENTRY,,"Enquiry screen is open"
T1,Unknown enquiry stays closed,Enter the id and the date,FT000 and 20261009,Both fields show the typed values
T1,Unknown enquiry stays closed,Run the enquiry,,Banner is No such customer
T2,Known enquiry opens the version,Enter the id and the date,FT2610090001 and 20261009,Both fields show the typed values
T2,Known enquiry opens the version,Run the enquiry,,Ben.name.client is directly under IBAN
```

That sample uses the usual Xray names. If the file they were given uses other names, keep their names. Only the three mapped meanings are fixed: identifier, summary, action.

A field that contains a comma or a line break is wrapped in straight `"` quotes. A quote inside the text is doubled (`""`).

## Fill it in Excel

1. Open the template they were given. Do not start from a blank workbook.
2. Paste the Copilot table into the rows under the header. If a header moved, stop and paste again.
3. Check one test by eye: same `TCID` on each of its steps, summary repeated, action filled, data and result filled or explicitly empty.
4. Save As **CSV UTF-8 (comma delimited)**.
5. If Excel offers only a semicolon CSV, either save that and set the importer delimiter to `;`, or set the list separator and save commas. Do not mix them.
6. Do not open the saved CSV in Excel again. Excel rewrites dates and encoding. Change the xlsx, then save the CSV once more.

Prompt to paste into Copilot, with the template attached:

```text
Fill this template. Do not change the header row. Do not add or remove columns.
One spreadsheet row per test step.
Repeat TCID and Test Summary on every step that belongs to the same test.
Leave a cell empty when the step has no data. Do not write "N/A".
Return a table I can paste under the header. No code fence. No extra commentary.
```

If Copilot returns a fence or new headers, reject that answer and paste again. Do not repair it by hand in the chat.

## Import

1. Tests menu → **Test Case Importer**. Not Jira's generic CSV import.
2. Setup: the delimiter and the encoding of the file you just saved.
3. Project: the Xray project. Set the date format only if a column contains dates. Format is Java `SimpleDateFormat`, for example `dd/MM/yyyy`.
4. Map `TCID` → Test Case Identifier, the summary column → Summary, `Action` → Action, and `Data` / `Result` to the step fields.
5. Map value lists (priority, component) when the CSV words are not already the Jira words.
6. Begin import.

A saved configuration from a previous import is reusable only when the header row did not change.

To update tests that already exist, the issue keys must be in the same project, the issues must already be Manual tests, and you need Create and Edit. The CSV replaces the whole step list of each updated test.

## When it still fails

| What you see | What to change |
|---|---|
| Every column lands in one field | Delimiter on the Setup page does not match the file. |
| Cyrillic (or any non-ASCII) is garbage | File and Setup page are not both UTF-8. |
| Tests are created with no steps, or each step is its own test | `TCID` is blank, or it changes on every row, or it was not mapped to Test Case Identifier. |
| Summary is required | The summary column was not mapped, or it is empty on a row that starts a new `TCID`. |
| Option / user / component not found | The cell is not an existing Jira value. Fix the cell. Do not add a column. |
| Importer menu is missing | The user lacks Bulk Change, or lacks Create Issues on the project. |
| Import button works and the test is still wrong | A required field on the Test screen was never a column. Add that column to the template once, then keep it. |

Put a unique label on the batch, for example `import-2026-10-10`, so a bad run can be found and deleted without touching older tests.

The filled test of the bench is `guides/xray-bench-execution.csv`. Do not copy an FSD use case into it.
