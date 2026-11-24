import { expect } from '@playwright/test';
import type { T24 } from '../t24/session';

/** One FT payment as a test supplies it. Field names are T24 names, verbatim. */
export interface FtInput {
  'DEBIT.ACCT.NO': string;
  'CREDIT.CURRENCY': string;
  'DEBIT.AMOUNT'?: string;
  'CREDIT.AMOUNT'?: string;
  'BENEF.NAME': string;
  [extra: string]: string | undefined;   // any further mandatory/local fields
}

export class FtPaymentPage {
  constructor(private t: T24, readonly version = process.env.T24_FT_VERSION ?? 'FT,BNK.OUT.EUR.PMNT.BR') {}

  async openNew() { await this.t.command(`${this.version} I`); await expect(this.t.field('DEBIT.ACCT.NO')).toBeEditable(); }
  async open(mode: 'A' | 'S', id: string) { await this.t.command(`${this.version} ${mode} ${id}`); }

  /** Order matters: debit account first (enrichment), then currency (vostro autoload), then the rest. */
  async fill(d: FtInput) {
    await this.t.set('DEBIT.ACCT.NO', d['DEBIT.ACCT.NO']);
    await this.t.set('CREDIT.CURRENCY', d['CREDIT.CURRENCY']);
    const rest = { ...d } as Record<string, string | undefined>;
    delete rest['DEBIT.ACCT.NO']; delete rest['CREDIT.CURRENCY'];
    await this.t.setMany(rest);
  }

  async input(d: FtInput, acceptOverrides = true) {
    await this.openNew();
    await this.fill(d);
    return this.t.validateAndCommit({ acceptOverrides });
  }

  async authorise(id: string) {
    await this.open('A', id);
    // Wait for the record screen itself; a key press would otherwise land on the previous document.
    await expect(this.t.inMain(this.t.p.recordStatus)).toBeVisible();
    await this.t.act('authorise');
    await expect(this.t.inMain(this.t.p.messages.complete).or(this.t.inMain(this.t.p.messages.error)).first()).toBeVisible();
    return this.t.messages();
  }

  async status(id: string) {
    await this.open('S', id);
    return (await this.t.inMain(this.t.p.recordStatus).innerText()).trim();
  }
}
