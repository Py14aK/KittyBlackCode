import { test, expect, inputter } from './fixtures';
import { readCsv } from '../src/util/csv';
import type { FtInput } from '../src/pages/FtPaymentPage';

// Data-driven validation matrix. Add rows to the CSV, not code.
// Expect: complete | error | override.  Contains: substring that must appear.
const cases = readCsv('data/cases/ft_field_rules.csv');

for (const c of cases) {
  test(`${c.Case} @${c.TCID}`, async ({ t24, ft }) => {
    await t24.login(inputter);
    await ft.openNew();
    const d: FtInput = {
      'DEBIT.ACCT.NO': c['DEBIT.ACCT.NO'], 'CREDIT.CURRENCY': c['CREDIT.CURRENCY'],
      'DEBIT.AMOUNT': c['DEBIT.AMOUNT'], 'CREDIT.AMOUNT': c['CREDIT.AMOUNT'], 'BENEF.NAME': c['BENEF.NAME'],
    };
    await ft.fill(d);
    const { id, msgs } = await t24.validateAndCommit({ acceptOverrides: false });
    await t24.evidence(`${c.TCID} after validate`);

    if (c.Expect === 'complete') {
      expect(msgs.errors, 'no errors expected').toEqual([]);
      expect(id).toMatch(/^FT\w+$/);
    } else if (c.Expect === 'error') {
      expect(id).toBeNull();
      expect(msgs.errors.join(' | ')).toContain(c.Contains);
    } else if (c.Expect === 'override') {
      expect(id).toBeNull();
      expect(msgs.errors).toEqual([]);
      expect(msgs.overrides.join(' | ')).toContain(c.Contains);
    } else throw new Error(`Unknown Expect "${c.Expect}" in CSV row ${c.TCID}`);
  });
}
