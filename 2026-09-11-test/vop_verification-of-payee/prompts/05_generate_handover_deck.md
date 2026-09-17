# Prompt — generate the missing handover deck

Paste into Copilot Chat with this folder open.
Load mindset: Kitty CORE KERNEL + this task only.

---

Generate exactly one file in this folder:

    UBB_VoP_Handover_2026-09-09.html

It is the PM/BA deck named by `HANDOVER.md` and `README.md`. One file, no build, no CDN, UTF-8, `lang="bg"`.

Read first, in order: `HANDOVER.md`, `README.md`, `EDITING.md`, `.github/copilot-instructions.md`, `docs/DECISIONS.md`, then the model and tests if they exist.

Twelve slides, no more:

1. Title. The row remains after the transfer. Working concept 09.09.2026. Not an approved FSD.
2. P1-P4 and legend ⊨ ≃ ↦ ⊥. Note: "втори request" vs second FT is ≃.
3. Three attributes (IBAN, name Latin VARCHAR 140, name Cyrillic VARCHAR 140). Codes MTCH CMTC NMTC NOAP. Internal route vs CUSTOMER / BG.NAME / Ben. Customer 1. Mark ⊥ if both routes are treated as one enquiry without V13.
4. Live enquiry simulator. Contract below.
5. Two-route SVG. Generate = new id. FT = selected id. Back adds one last row.
6. Fields and states. Empty `ft_reference` proves nothing.
7. V01-V13 as on-screen toggles only. Do not persist. Do not write `docs/DECISIONS.md`.
8. AC01-AC16 table. Name the blocking Vxx.
9. Ordinary vs agent. Machine does not fill V-ids.
10. QT-2-4A audit only if you observed it this run. Otherwise keep the FSD-discipline point and invent no findings.
11. BRD/FSD/ADR/AC/CI map.
12. Next blockers: V01, V03, V04, V07.

Simulator:

- Start with VOP-0001..0003 with FT, VOP-0004 NMTC without FT, plus one last row `— нов —`.
- Generate from last row = new id (R06). Generate from a stored row = new id, do not overwrite source (R07).
- FT disabled on the last row (R03). Existing FT blocks (R09). NMTC/NOAP stop and name V07. Success writes FT on the same row (R08).
- No network. No storage.

Visual: paper `#F1F3EF`, ink `#161F27`, stamp `#9E2B25`, ok `#2B6446`. Serif body, mono for codes and the T24 panel. Sticky rail, fixed prev/next, arrow keys.

Protected strings, byte-for-byte: VoP, T24, FT, IBAN, MTCH, CMTC, NMTC, NOAP, POP ID, OpenID, Check ID, Borica, FUNDS.TRANSFER, Ben. Customer 1, BG.NAME, CUSTOMER, and every Vxx / ACxx / Rxx already in this folder.

Do not fill a decision. Do not add NMTC or NOAP to admissible. Do not invent ticket keys, staff names, or hostnames. Do not claim T24 was tested.

When the file is written, stop. In chat: slide count, confirm last-row and FT-block exist in the script, then the verification footer from the kernel.
