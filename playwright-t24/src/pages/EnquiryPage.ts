import { expect } from '@playwright/test';
import type { T24 } from '../t24/session';

export type Row = Record<string, string>;

export class EnquiryPage {
  constructor(private t: T24) {}

  /** Runs "ENQ <name>", fills selection fields, returns rows as objects keyed by column header. */
  async run(name: string, selection: Record<string, string>): Promise<{ rows: Row[]; errors: string[] }> {
    await this.t.command(`ENQ ${name}`);
    for (const [k, v] of Object.entries(selection)) await this.t.set(k, v);
    await this.t.inMain(this.t.p.enquiry.run).click();
    const table = this.t.inMain(this.t.p.enquiry.results);
    await expect(table.or(this.t.inMain(this.t.p.messages.error)).first()).toBeVisible();
    const errors = (await this.t.messages()).errors;
    if (errors.length) return { rows: [], errors };
    return { rows: await this.rows(), errors };
  }

  async rows(): Promise<Row[]> {
    const table = this.t.inMain(this.t.p.enquiry.results);
    const head = (await table.locator('tr').first().locator('th').allInnerTexts()).map((s) => s.trim());
    const out: Row[] = [];
    const trs = table.locator('tr');
    for (let i = 1; i < (await trs.count()); i++) {
      const cells = (await trs.nth(i).locator('td').allInnerTexts()).map((s) => s.trim());
      out.push(Object.fromEntries(head.map((h, j) => [h, cells[j] ?? ''])));
    }
    return out;
  }

  /** Attribute payload on a result cell, e.g. a base64 XML message. */
  async cellData(row: number, col: number, attr: string) {
    return this.t.inMain(this.t.p.enquiry.results).locator('tr').nth(row + 1).locator('td').nth(col).getAttribute(attr);
  }
}
