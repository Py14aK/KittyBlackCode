import { test, expect, inputter, authoriser } from './fixtures';
import { b64decode, parseXml, get } from '../src/util/codec';

const H_SERVICE = process.env.T24_H_SERVICE ?? 'BNK.H.TRANSFER';
const TODAY = process.env.T24_TODAY ?? '20261028';   // T24 business date, not the wall clock

test('FT outgoing EUR: input, authorise, enquiry, H table, XML @TKT-00001', async ({ t24, ft, enq, ts }) => {
  const benef = 'ПЪРВИ БЕНЕФИЦИЕНТ ООД';            // Cyrillic on purpose: encoding check end to end
  let id = '';

  await test.step('inputter enters and commits the payment', async () => {
    await t24.login(inputter);
    const r = await ft.input({ 'DEBIT.ACCT.NO': '10000001', 'CREDIT.CURRENCY': 'EUR', 'DEBIT.AMOUNT': '250.00', 'BENEF.NAME': benef });
    expect(r.msgs.errors).toEqual([]);
    expect(r.id).toMatch(/^FT\w+$/);
    id = r.id!;
    await t24.evidence(`input ${id}`);
  });

  await test.step('enrichment routines filled dependent fields', async () => {
    await ft.open('S', id);
    await expect(t24.field('DEBIT.CURRENCY')).toHaveValue('EUR');
    await expect(t24.field('CREDIT.ACCT.NO')).toHaveValue(/^EUR/);
  });

  await test.step('four-eyes: inputter cannot authorise own record', async () => {
    const m = await ft.authorise(id);
    expect(m.errors.join(' ')).toMatch(/SAME.USER/);
    await t24.logout();
  });

  await test.step('authoriser authorises', async () => {
    await t24.login(authoriser);
    const m = await ft.authorise(id);
    expect(m.errors).toEqual([]);
    expect(t24.idFrom(m.complete)).toBe(id);
    expect(await ft.status(id)).toBe('AUTH');
    await t24.evidence(`authorised ${id}`);
  });

  await test.step('accounting entries visible in ENQ TXN.ENTRY', async () => {
    const { rows, errors } = await enq.run('TXN.ENTRY', { 'TRANSACTION.REF': id, 'BOOKING.DATE': TODAY });
    expect(errors).toEqual([]);
    expect(rows.map((r) => r.SIGN).sort()).toEqual(['C', 'D']);
    await t24.evidence(`TXN.ENTRY ${id}`);
  });

  await test.step('service on, payment reaches H table with XML', async () => {
    expect(await ts.ensure(H_SERVICE, 'START')).toBe('START');
    const { rows } = await enq.run('H.TRANSFER', { 'TRANSACTION.REF': id });
    expect(rows[0].STATUS).toBe('SENT');
    const xml = b64decode((await enq.cellData(0, 2, 'data-b64'))!);
    const doc = parseXml(xml);
    const tx = get(doc, 'Document.FIToFICstmrCdtTrf.CdtTrfTxInf');
    expect(get(tx, 'PmtId.EndToEndId')).toBe(id);
    expect(get(tx, 'IntrBkSttlmAmt.#text')).toBe(250);
    expect(get(tx, 'IntrBkSttlmAmt.@Ccy')).toBe('EUR');
    expect(get(tx, 'Cdtr.Nm')).toBe(benef);
    await test.info().attach(`${id}.xml`, { body: xml, contentType: 'application/xml' });
    await t24.evidence(`H.TRANSFER ${id}`);
  });
});

test('service stopped: payment stays PENDING, no XML @TKT-00002', async ({ t24, ft, enq, ts }) => {
  await t24.login(inputter);
  const { id } = await ft.input({ 'DEBIT.ACCT.NO': '10000001', 'CREDIT.CURRENCY': 'EUR', 'DEBIT.AMOUNT': '10.00', 'BENEF.NAME': 'X' });
  await t24.logout();
  await t24.login(authoriser);
  await ft.authorise(id!);
  await ts.ensure(H_SERVICE, 'STOP');
  const { rows } = await enq.run('H.TRANSFER', { 'TRANSACTION.REF': id! });
  expect(rows[0].STATUS).toBe('PENDING');
  expect(await enq.cellData(0, 2, 'data-b64')).toBeNull();
});
