# Worked examples

## Example A user turn
MODE /DO FSD_ID UBBPMINTL with Word/BRD pasted and CATALOG_SLICE NOT SUPPLIED.

## Example B catalog missing
05_CARDS uses FIELD UNMATCHED APP FUNDS.TRANSFER.UBB.EUR.PMT.BG.BR NOTES NEED FROM CATALOG.
Owner Antonio epic TSC-17852. Related TSC-46436 Reni and TSC-46573 Antonio stay out of this folder.

## Example C catalog present
Only tokens that were in the pasted rows. One APP per FIELD block. BENEF.IBAN BENEF.CYRNAME RESPONSE.VOP on FUNDS.TRANSFER.UBB.EUR.PMT.BG.BR.

## Example D collision
UBBPMDD TSC-17855. COLLISION with UBBCSHMN correction. Do not merge.

## Example E reject
FIELD_1_NAME BEN.NAME.CYR and two versions in one APP cell.
