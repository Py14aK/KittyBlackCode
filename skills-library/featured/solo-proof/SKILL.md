---
name: "solo-proof"
description: "Use when asked to work one hard mathematics problem to a written proof: reason in stages, save each settled step to a notes file so nothing is lost if a reply is cut off, and finish with a self-contained proof.md a referee can read alone."
---

# Solo proof

Solve one hard mathematics problem yourself, in this conversation, with a notes file as durable memory and a self-contained proof.md as the deliverable.

## Setup

1. Take the problem exactly as the user gave it (pasted text or an attached file). If no problem is given, ask for it in one sentence and stop.
2. Make a run folder in the working directory, `math-proof-<short-slug>/`, holding:
   - `problem.md`: the problem, verbatim. Nothing added, removed or reworded. This is the authoritative statement.
   - `notes.md`: your working notes.
   - `proof.md`: the deliverable.
3. If the folder already exists with the same problem: read notes.md (and proof.md if present). If proof.md is complete and nothing is left in the notes, say where it is and stop. Otherwise continue from the last recorded point; never start over. If it holds a different problem, use a new folder.

## Working rule: write as you go

Each reply has a bounded output allowance that also covers private reasoning, and it is far smaller than a hard problem deserves. Only what is written to a file is guaranteed to survive into the next reply. So:

- Early in every reply, before any long derivation, write the current plan and the precise statement now being attempted to notes.md.
- Reason toward the next concrete intermediate result. As soon as you have it, append it to notes.md, then continue.
- Record dead ends with the reason they fail. They are results too.
- Many short written steps beat one long unwritten one.
- If a reply is cut off, re-read notes.md at the start of the next and continue from the last written line.
- A partial answer is far more useful than none. Writing to notes is not finishing; keep going after each write.

What to record in notes.md: definitions fixed, reductions, lemmas with full proofs, counterexamples found, the exact statement currently targeted, open gaps, and verification of small cases.

## Checks while working

Where a computational check is possible, use it: small cases by brute force, symbolic simplification (SymPy or Wolfram), numerical evaluation of a claimed identity. A check supports a step; it does not replace the proof. Note in notes.md which steps were checked and how.

## Deliverable: proof.md

When the problem is resolved, or taken as far as possible, write proof.md. It is read alone by a referee who cannot open notes.md or anything else, so it must be self-contained:

- Restate the problem.
- State the result proved (full resolution, or exactly what is proved and what remains open).
- Give every argument in full: definitions, lemmas with proofs, the main proof. No "see notes".
- Mark clearly any step that is only checked numerically or is conjectural.

Work unattended: do not stop to ask questions once the problem is stated.

## Final reply

Briefly: where proof.md is, and whether it resolves the problem completely or, in proof.md's own words, what it leaves open.