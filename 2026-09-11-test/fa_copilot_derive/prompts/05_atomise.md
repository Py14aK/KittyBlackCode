# Prompt — atomise a document

---

Read the attached document and emit atoms as TSV rows matching
`data/atoms_vop_2026-09-11.tsv`.

Rules:

1. One behavioural claim per row. If a sentence carries two obligations, it is
   two atoms.
2. `source` is `BRD` for a contracted requirement, `FSD_S8` for a solution
   claim, `T24` for observed behaviour. Never guess the source from tone.
3. `subject` is the join key. Use `area.thing` form, reuse an existing subject
   whenever the atom is about the same thing, and say so when you do.
4. `assertion` is normalised: present tense, active, one obligation. Two
   sources that agree must produce byte-identical assertions, or the
   triangulation will report drift that is not there.
5. `anchor` is the section or page. An atom without an anchor is rejected.
6. Never invent an atom to fill a gap. A missing atom is a finding.

Then run `python src/run_derive_2026_09_11.py data/<your file>.tsv` and paste
the triangulation block.

Report separately: how many atoms, which subjects appear in only one source,
and which assertions you had to normalise heavily — heavy normalisation is
where you may have flattened a real difference.
