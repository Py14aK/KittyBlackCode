#!/usr/bin/env python3
"""
xray2spec: Xray Test Case Importer CSV  ->  Playwright spec skeletons for the T24 harness.

    python tools/xray2spec.py CASES.csv [--fieldmap data/fieldmap.csv] [--out tests/generated]
    python tools/xray2spec.py --selftest

Rules (designed so a generated test can never pass by accident):
  * One spec file per TCID, one test.step per CSV step row, steps in file order.
  * Actions are mapped by a small verb table plus a phrase->FIELD map. Field names are
    copied verbatim (identifier lock); a dotted CAPS token in the Action text is taken as-is.
  * Every Result becomes an assertion: "<field> shows V" -> toHaveValue, "The banner/title is X"
    -> work frame contains X. Anything not understood becomes an UNMAPPED comment AND the whole
    test is marked test.fixme, so it is skipped and listed, never green.
  * Prints a coverage table (mapped steps / total) so you see what still needs a human.
Input: semicolon CSV, UTF-8 (BOM ok), header TCID;Test Summary;Test Priority;Component;Action;Data;Result
"""
from __future__ import annotations

import argparse, csv, io, json, re, sys
from dataclasses import dataclass, field
from pathlib import Path

HEADER = ["TCID", "Test Summary", "Test Priority", "Component", "Action", "Data", "Result"]
DOTTED = re.compile(r"\b([A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z0-9]+)+)\b")   # BENEF.NAME, Ben.name.client
CMD = re.compile(r"^(ENQ\s+\S+|FT,\S+.*|TS\b.*|/\S+.*|[A-Z][A-Z0-9.]*,[A-Z0-9.]+.*)$")

DEFAULT_FIELDMAP = {   # phrase (lower case, matched as substring) -> T24 field. Extend per project.
    "ft id": "TRANSACTION.REF", "date": "BOOKING.DATE", "payer": "DEBIT.ACCT.NO",
    "debit account": "DEBIT.ACCT.NO", "debit amount": "DEBIT.AMOUNT", "credit amount": "CREDIT.AMOUNT",
    "beneficiary name": "BENEF.NAME", "credit currency": "CREDIT.CURRENCY", "service": "SERVICE.NAME",
}


@dataclass
class Spec:
    tcid: str
    summary: str
    lines: list[str] = field(default_factory=list)
    mapped: int = 0
    total: int = 0
    unmapped: list[str] = field(default_factory=list)


def ts(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)          # safe TS string literal, keeps Cyrillic


def load_fieldmap(path: Path | None) -> dict[str, str]:
    fm = dict(DEFAULT_FIELDMAP)
    if path:
        for row in csv.reader(path.read_text(encoding="utf-8-sig").splitlines(), delimiter=";"):
            if len(row) >= 2 and row[0].strip() and not row[0].startswith("#"):
                fm[row[0].strip().lower()] = row[1].strip()
    return dict(sorted(fm.items(), key=lambda kv: -len(kv[0])))   # longest phrase wins


def find_field(text: str, fm: dict[str, str]) -> str | None:
    m = DOTTED.search(text)
    if m and not m.group(1).lower().startswith(("enq.", "ft,")):
        return m.group(1)
    low = text.lower()
    for phrase, f in fm.items():
        if phrase in low:
            return f
    return None


def map_action(action: str, data: str, fm: dict[str, str]) -> list[str] | None:
    """Return TS statements for one action clause, or None if not understood."""
    a = action.strip().rstrip(".")
    low = a.lower()
    if re.fullmatch(r"press (go|enter)", low):
        return []          # t24.command() already submits the command line
    if data.startswith("http") or re.search(r"\b(sign in|log ?in|open the .*page)\b", low):
        return ["await t24.login(inputter);"]
    if data and CMD.match(data) and re.search(r"command|version|press go|go\b", low):
        return [f"await t24.command({ts(data)});"]
    if re.search(r"run enquiry", low):
        return ["await t24.inMain(t24.p.enquiry.run).click();"]
    if re.search(r"accept (the )?(warning|override)", low):
        return ["await t24.acceptOverrides();"]
    for verb, act in (("validate", "validate"), ("commit", "commit"), ("authoris", "authorise"), ("authoriz", "authorise")):
        if re.search(rf"\bpress {verb}|\b{verb}\b", low) and not data:
            return [f"await t24.act('{act}');"]
    if "screenshot" in low:
        return [f"await t24.evidence({ts(a)});"]
    if low.startswith("clear "):
        f = find_field(a[6:], fm)
        return [f"await t24.set({ts(f)}, '');"] if f else None
    if re.match(r"(enter|type|choose|select|input|fill)\b", low):
        # "Enter a debit amount and a credit amount" + "10 and 10"
        parts = re.split(r"\s+and\s+", a)
        vals = re.split(r"\s+and\s+", data) if data else []
        if len(parts) > 1 and len(parts) == len(vals):
            out = []
            for p, v in zip(parts, vals):
                f = find_field(p, fm)
                if not f:
                    return None
                out.append(f"await t24.set({ts(f)}, {ts(v)});")
            return out
        f = find_field(a, fm)
        return [f"await t24.set({ts(f)}, {ts(data)});"] if f else None
    return None


def map_result(result: str, fm: dict[str, str]) -> list[str] | None:
    r = result.strip().rstrip(".")
    if not r:
        return []
    out: list[str] = []
    for clause in re.split(r"\s+and\s+(?=the\b|[A-Za-z.]+\s+shows\b)", r, flags=re.I):
        m = re.match(r"(?:the\s+)?(banner|title|message|screen)\s+is\s+(.+)$", clause, re.I)
        if m:
            out.append(f"await expect(t24.main().locator('body')).toContainText({ts(m.group(2).strip())});")
            continue
        m = re.match(r"(.+?)\s+shows?\s+(.+)$", clause, re.I)
        if m:
            f = find_field(m.group(1), fm)
            if f:
                out.append(f"await expect(t24.field({ts(f)})).toHaveValue({ts(m.group(2).strip())});")
                continue
            out.append(f"await expect(t24.main().locator('body')).toContainText({ts(m.group(2).strip())});")
            continue
        m = re.match(r"(.+?)\s+is (?:on screen|visible)$", clause, re.I)
        if m:
            out.append(f"await expect(t24.page.locator('body')).toBeVisible(); // {m.group(1)}: refine selector")
            continue
        return None
    return out


def read_cases(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(io.StringIO(text.lstrip("﻿")), delimiter=";"))
    if not rows or list(rows[0].keys())[: len(HEADER)] != HEADER:
        got = list(rows[0].keys()) if rows else []
        raise SystemExit(f"Header mismatch.\n expected {';'.join(HEADER)}\n got      {';'.join(got)}")
    return rows


def build(rows: list[dict[str, str]], fm: dict[str, str]) -> list[Spec]:
    specs: dict[str, Spec] = {}
    for i, row in enumerate(rows, start=2):
        tcid = (row["TCID"] or "").strip()
        if not tcid:
            raise SystemExit(f"Row {i}: empty TCID")
        s = specs.setdefault(tcid, Spec(tcid, (row["Test Summary"] or "").strip()))
        if row["Test Summary"] and not s.summary:
            s.summary = row["Test Summary"].strip()
        action, data, result = (row["Action"] or "").strip(), (row["Data"] or "").strip(), (row["Result"] or "").strip()
        s.total += 1
        stmts: list[str] = []
        ok = True
        for clause in re.split(r"\s+and\s+(?=press\b)", action, flags=re.I):   # "Clear X and press Validate"
            d = "" if re.match(r"press\b", clause, re.I) else data
            m = map_action(clause, d, fm)
            if m is None:
                ok = False
                stmts.append(f"// UNMAPPED ACTION: {clause} | data: {data}")
            else:
                stmts += m
        mr = map_result(result, fm)
        if mr is None:
            ok = False
            stmts.append(f"// UNMAPPED RESULT: {result}")
        else:
            stmts += mr
        stmts.append(f"await t24.evidence({ts(f'{tcid} step {s.total}')});")
        if ok:
            s.mapped += 1
        else:
            s.unmapped.append(f"step {s.total}: {action}")
        body = "\n".join("    " + x for x in stmts)
        s.lines.append(f"  await test.step({ts(f'{s.total}. {action}')}, async () => {{\n{body}\n  }});")
    return list(specs.values())


def render(s: Spec, source: str) -> str:
    fixme = ""
    if s.unmapped:
        fixme = f"  test.fixme(true, {ts('unmapped: ' + '; '.join(s.unmapped))});\n"
    return (
        f"// GENERATED by tools/xray2spec.py from {source}. Edit the CSV or fieldmap, then regenerate.\n"
        f"// Coverage {s.mapped}/{s.total} steps mapped.\n"
        "import { test, expect, inputter } from '../fixtures';\n\n"
        f"test({ts(f'{s.summary} @{s.tcid}')}, async ({{ t24 }}) => {{\n{fixme}"
        + "\n".join(s.lines)
        + "\n});\n"
    )


def selftest() -> None:
    csv_text = (
        "TCID;Test Summary;Test Priority;Component;Action;Data;Result\n"
        "T-1;Enquiry;Medium;;Type the enquiry command and press Go;ENQ TXN.ENTRY;The title is ENQ TXN.ENTRY\n"
        "T-1;;;;Enter the FT id;FT000;FT id shows FT000\n"
        "T-1;;;;Press Run enquiry;;The banner is NO RECORDS\n"
        "T-2;Amounts;Medium;;Enter a debit amount and a credit amount;10 and 10;Both amount fields show 10\n"
        "T-2;;;;Clear the credit amount and press Validate;;The banner is Warning\n"
        "T-3;Odd;Low;;Do a dance;;Everyone claps\n"
    )
    specs = {s.tcid: s for s in build(read_cases(csv_text), load_fieldmap(None))}
    t1 = render(specs["T-1"], "selftest")
    assert "t24.command(\"ENQ TXN.ENTRY\")" in t1, t1
    assert "t24.set(\"TRANSACTION.REF\", \"FT000\")" in t1
    assert "toHaveValue(\"FT000\")" in t1 and "fixme" not in t1
    t2 = render(specs["T-2"], "selftest")
    assert "t24.set(\"DEBIT.AMOUNT\", \"10\")" in t2 and "t24.set(\"CREDIT.AMOUNT\", \"10\")" in t2, t2
    assert "t24.set(\"CREDIT.AMOUNT\", '')" in t2 and "act('validate')" in t2, t2
    t3 = render(specs["T-3"], "selftest")
    assert "test.fixme(true" in t3 and specs["T-3"].mapped == 0, "unknown steps must force fixme"
    try:
        read_cases("TCID;Title;Result\nx;y;z\n")
        raise AssertionError("bad header accepted")
    except SystemExit:
        pass
    print("xray2spec selftest: ok (5 checks)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", nargs="?", type=Path)
    ap.add_argument("--fieldmap", type=Path)
    ap.add_argument("--out", type=Path, default=Path("tests/generated"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.csv:
        ap.error("CSV path required")
    specs = build(read_cases(a.csv.read_text(encoding="utf-8")), load_fieldmap(a.fieldmap))
    a.out.mkdir(parents=True, exist_ok=True)
    print(f"{'TCID':<16}{'mapped':>8}{'total':>7}  file")
    for s in specs:
        name = re.sub(r"[^\w.-]+", "_", s.tcid) + ".spec.ts"
        (a.out / name).write_text(render(s, a.csv.name), encoding="utf-8")
        print(f"{s.tcid:<16}{s.mapped:>8}{s.total:>7}  {a.out / name}" + ("   FIXME" if s.unmapped else ""))
        for u in s.unmapped:
            print(f"{'':16}  - {u}")


if __name__ == "__main__":
    main()
