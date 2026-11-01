#!/usr/bin/env python3
"""
xsd_check: validate XML messages (plain or base64) against an XSD, e.g. ISO 20022 pacs.008.

    python tools/xsd_check.py SCHEMA.xsd msg1.xml [msg2.b64 ...]
    python tools/xsd_check.py SCHEMA.xsd --b64 "PD94bWwg..."      # payload copied from a T24 screen
    python tools/xsd_check.py --selftest

Exit code 0 = all valid, 1 = at least one invalid, 2 = usage/schema error.
The XSD comes from the bank's scheme pack; it is never fetched from the network (closed SYT).
"""
import argparse, base64, binascii, sys
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    sys.exit("lxml missing: pip install lxml  (offline: pip download lxml on a connected machine, carry the wheel)")


def load_payload(raw: bytes) -> bytes:
    s = raw.strip()
    if s.startswith(b"<"):
        return s
    try:
        return base64.b64decode(s, validate=True)
    except binascii.Error as e:
        raise ValueError(f"neither XML nor valid base64: {e}")


def check(schema: "etree.XMLSchema", payload: bytes, label: str) -> bool:
    try:
        doc = etree.fromstring(payload, parser=etree.XMLParser(resolve_entities=False, no_network=True))
    except etree.XMLSyntaxError as e:
        print(f"FAIL {label}: not well-formed: {e}")
        return False
    if schema.validate(doc):
        print(f"OK   {label}")
        return True
    for err in schema.error_log:
        print(f"FAIL {label}: line {err.line}: {err.message}")
    return False


def selftest() -> None:
    xsd = b"""<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" targetNamespace="urn:t" xmlns="urn:t" elementFormDefault="qualified">
      <xs:element name="Doc"><xs:complexType><xs:sequence>
        <xs:element name="Id" type="xs:string"/>
        <xs:element name="Amt"><xs:simpleType><xs:restriction base="xs:decimal"><xs:fractionDigits value="2"/></xs:restriction></xs:simpleType></xs:element>
      </xs:sequence></xs:complexType></xs:element></xs:schema>"""
    schema = etree.XMLSchema(etree.fromstring(xsd))
    good = '<Doc xmlns="urn:t"><Id>FT1 Иван</Id><Amt>1.50</Amt></Doc>'.encode()
    bad = b'<Doc xmlns="urn:t"><Id>FT1</Id><Amt>1.505</Amt></Doc>'
    assert check(schema, load_payload(good), "good")
    assert check(schema, load_payload(base64.b64encode(good)), "good-b64")
    assert not check(schema, load_payload(bad), "bad-fraction")
    try:
        load_payload(b"!!notbase64!!")
        raise AssertionError("garbage accepted")
    except ValueError:
        pass
    print("xsd_check selftest: ok (4 checks)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xsd", nargs="?", type=Path)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--b64", action="append", default=[], help="inline base64 payload (repeatable)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0
    if not a.xsd or not (a.files or a.b64):
        ap.print_usage()
        return 2
    try:
        schema = etree.XMLSchema(etree.parse(str(a.xsd)))
    except (etree.XMLSchemaParseError, OSError) as e:
        print(f"schema error: {e}")
        return 2
    ok = True
    for f in a.files:
        ok &= check(schema, load_payload(f.read_bytes()), str(f))
    for i, s in enumerate(a.b64, 1):
        ok &= check(schema, load_payload(s.encode()), f"inline#{i}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
