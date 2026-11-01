import { test, expect } from '@playwright/test';
import { b64encode, b64decode, parseXml, get } from '../src/util/codec';

test('base64 round trip keeps Cyrillic', () => {
  const s = 'ПЪРВИ СРЕДЕН ПОСЛЕДЕН / Ünïcode';
  expect(b64decode(b64encode(s))).toBe(s);
});
test('malformed XML throws with position', () => {
  expect(() => parseXml('<a><b></a>')).toThrow(/Malformed XML at \d+:\d+/);
});
test('namespace prefix stripped, attributes kept', () => {
  const d = parseXml('<x:Doc xmlns:x="urn:a"><x:Amt Ccy="EUR">1.50</x:Amt></x:Doc>');
  expect(get(d, 'Doc.Amt.@Ccy')).toBe('EUR');
});
