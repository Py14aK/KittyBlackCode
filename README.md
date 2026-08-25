,,/
Jira Daily Snapshot + Action Extraction Agent

Purpose

Automate the repetitive work around the team's daily Jira review spreadsheet.

The current process uses a monthly Excel workbook such as:

"~ Payment July daily.xlsx"

Each worksheet represents one working day.

The team reviews tickets one by one during the daily meeting. The sheet acts simultaneously as:

- a Jira status snapshot
- meeting notes
- an action list
- evidence of what changed
- input for the status sent to the PM

One column, for example "fixver_1", may contain free-text comments such as:

"He will write an email to X."

Those comments frequently contain hidden TODOs.

The aim is to turn the existing spreadsheet into a lightweight agentic workflow without replacing the team's current process.

---

1. Daily Input

Use:

1. Today's Jira/JQL snapshot.
2. Yesterday's worksheet.
3. Today's new worksheet.
4. Existing ticket comments/status fields.
5. Relevant attachments or test evidence where accessible.

Do not require the team to maintain a second tracking system.

The Excel workbook remains the visible operational artifact.

---

2. Create Today's Sheet

Create today's worksheet from the newest Jira snapshot.

Use the Jira ticket key as the stable identifier.

For each ticket:

"Jira Key → match yesterday's row → transfer persistent context"

Use "XLOOKUP", equivalent matching logic, or programmatic matching.

Example concept:

=XLOOKUP(
    [@Jira],
    Yesterday!JiraColumn,
    Yesterday!CommentColumn,
    ""
)

---

3. Carry Forward Useful Context

For tickets that already existed yesterday:

Carry forward unresolved notes/actions where today's Jira data does not supersede them.

Do not blindly copy everything.

Distinguish between:

- historical status
- still-active action
- completed action
- new status
- new decision

If today's comment field is empty but yesterday contained an unresolved action, keep the unresolved action visible.

---

4. Detect New Tickets

Compare today's Jira keys with yesterday's.

If:

"ticket_today ∉ tickets_yesterday"

mark it:

"NEW"

Optionally also extract:

- assignee
- priority
- issue type
- creation date
- current status
- latest comment

---

5. Detect Changed Tickets

For existing tickets, detect meaningful changes in:

- Jira status
- assignee
- priority
- Fix Version
- latest comment
- blocker
- due date
- test state

Mark tickets whose state changed since yesterday.

Do not flag formatting-only differences as meaningful changes.

---

6. Extract TODOs from Comments

The most important AI task is to distinguish narrative status from an actual commitment.

Examples:

Antonio will email the bank.
Waiting for DEV to investigate.
Need confirmation from UAT.
Neda will execute the tests.
Send the XML example to the developer.
Ask for a new local field.

Convert these into structured actions:

Ticket
Action
Owner
Recipient / Dependency
Status
Evidence needed
Due date
Source comment

Example:

TSC-12345
Send email requesting UAT confirmation
Antonio
UAT team
OPEN
Email sent / reply received
Not specified
"Antonio will email UAT for confirmation."

Do not invent an owner if one cannot be inferred reliably.

Use:

"UNKNOWN"

instead.

---

7. Separate Status from Action

For every extracted comment classify content as:

STATUS

Information about what is currently true.

Example:

"Development finished and deployed to SYT."

DECISION

Something the team agreed.

Example:

"Agreed to test TARGET before moving to UAT."

ACTION

Something someone must still do.

Example:

"Send updated XML to DEV."

BLOCKER

Something preventing progress.

Example:

"Waiting for bank confirmation."

One comment may contain several categories.

---

8. Generate Personal TODO Lists

After the meeting, generate a TODO list per owner.

Example:

OWNER: Antonio

TSC-41246
- Run DEV comparison.
- Check parameterisation.
- Send findings to DEV.

TSC-xxxxx
- Prepare UAT email.
- Attach test evidence.

The source Jira ticket must always remain attached to the action.

Never create orphan TODOs.

---

9. Prepare Emails Automatically

If a meeting comment creates an email action:

"Antonio will email X."

the agent should prepare a draft.

The draft should use:

- ticket context
- latest status
- exact technical strings
- relevant test evidence
- requested action

But:

draft only

Do not send automatically without explicit approval.

Example workflow:

Meeting comment
      ↓
Action extraction
      ↓
Recipient/context resolution
      ↓
Draft email
      ↓
Human review
      ↓
Send

---

10. Test-Evidence Assistance

Where available, the agent should locate the evidence needed for the action.

Examples:

- XML examples
- screenshots
- test cases
- Jira comments
- previous emails
- FSD sections
- BRD sections
- UAT/SYT/DEV results

For technical issues, summarize evidence as:

Environment
Scenario
Input
Observed result
Expected result
Evidence location

Do not claim evidence exists unless it was actually found.

---

11. Daily Meeting View

Generate a compact meeting view.

Preferred format:

Ticket | Current State | Evidence | Blocker | Next Action | Owner

The goal is rapid ticket-by-ticket discussion.

Avoid paragraphs.

The AI should not dominate the meeting with a large generated report.

---

12. PM Snapshot

After the meeting, produce a concise status snapshot suitable for sending to the PM.

Use:

Current state → Blocker/Risk → Next action

Include only material changes.

Do not repeat unchanged historical detail.

---

13. Daily Workbook Flow

Conceptually:

                Jira / JQL
                    │
                    ▼
             Today's snapshot
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
 Yesterday sheet         Compare tickets
          │                   │
          └─────────┬─────────┘
                    ▼
               Today's sheet
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   New tickets    Changes      Carry-over
                                 actions
                    │
                    ▼
              Meeting comments
                    │
                    ▼
            AI action extraction
                    │
       ┌────────────┼─────────────┐
       ▼            ▼             ▼
     TODOs       Email drafts   Evidence needs
       │            │             │
       └────────────┼─────────────┘
                    ▼
               PM snapshot

---

14. Human Approval Gates

AI may automatically:

- compare worksheets
- classify comments
- detect ticket changes
- extract candidate actions
- prepare TODO lists
- prepare email drafts
- summarize test evidence
- prepare PM status

AI must not automatically:

- send external emails
- update Jira ticket status
- change ownership
- alter deadlines
- mark actions complete
- approve tests
- interpret ambiguous decisions as final

without explicit human approval.

---

15. Evidence Requirement

Every AI-generated action should retain provenance.

Minimum:

Ticket:
Source:
Source text:
Extracted action:
Confidence:

For example:

Ticket: TSC-41246
Source: Daily sheet 2026-08-14 / fixver_1
Source text: "Will check in DEV and send result."
Extracted action: Check scenario in DEV and report result.
Confidence: High

This prevents the AI layer from quietly inventing work.

---

16. Useful Output Files

The workflow can generate:

Daily sheet

The existing Excel operational view.

"todo_today.txt"

TSC-xxxxx
[ ] Action
[ ] Action

TSC-yyyyy
[ ] Action

"email_drafts/"

Draft messages triggered by meeting commitments.

"changes_today.txt"

Only tickets materially changed since yesterday.

"pm_status.txt"

Compact final status.

---

17. First Implementation

Do not begin with a large autonomous Jira agent.

Start with:

Existing Excel
+
yesterday/today comparison
+
TODO extraction
+
draft-email generation

This captures most of the useful automation while keeping the existing team workflow unchanged.

Once this works reliably, Jira API/JQL integration can replace manual snapshot import.

---

18. Success Criteria

The system is useful if it measurably reduces:

- manual copying between daily worksheets
- forgotten meeting actions
- time spent reconstructing ticket context
- repetitive email drafting
- missed ownership
- time needed to prepare the PM update

It is not successful merely because it can generate a polished dashboard.

The primary objective is:

Turn the comments the team already writes into reliable, traceable next actions without creating another administrative system.