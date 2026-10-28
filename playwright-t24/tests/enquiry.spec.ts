import { test, expect, inputter } from './fixtures';

test('TXN.ENTRY unknown FT gives no records @TKT-00003', async ({ t24, enq }) => {
  await t24.login(inputter);
  const r = await enq.run('TXN.ENTRY', { 'TRANSACTION.REF': 'FT00000000000', 'BOOKING.DATE': '20261009' });
  expect(r.rows).toEqual([]);
  expect(r.errors.join(' ')).toMatch(/NO RECORDS/);
  await t24.evidence('no records');
});

test('TXN.ENTRY rejects date not in YYYYMMDD @TKT-00004', async ({ t24, enq }) => {
  await t24.login(inputter);
  const r = await enq.run('TXN.ENTRY', { 'TRANSACTION.REF': 'FT00000000000', 'BOOKING.DATE': '09.10.2026' });
  expect(r.errors.join(' ')).toMatch(/DATE/);
});
