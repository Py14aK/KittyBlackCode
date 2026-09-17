# Prompt — load UAT observations

Use after someone has actually run the scenarios in T24.

---

Here are the observed results: <paste, or attach the UAT log>

1. Emit `T24` atoms. `assertion` describes what the system *did*, not what it
   should have done. If the observation is ambiguous, say so and emit nothing
   for that subject.
2. Append them to the atom file. Change no existing row.
3. Re-run the derivation and paste the before-and-after counts.
4. For every subject that became `DEFECT` or `CLAIM_WRONG`, state which of the
   three sources you believe is wrong, and why. Do not assume the system is
   wrong; the FSD is wrong roughly as often.

Do not delete atoms to make a verdict change. If a verdict looks wrong, the
fix is a new atom with an anchor, not an edited one.
