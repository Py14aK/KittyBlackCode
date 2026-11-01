import { expect } from '@playwright/test';
import type { T24 } from '../t24/session';

/** TS command: load a TSA.SERVICE, read status, START/STOP it. */
export class ServicesPage {
  constructor(private t: T24) {}
  private s() { return this.t.p.services; }

  async status(service: string) {
    await this.t.command('TS');
    await this.t.inMain(this.s().name).fill(service);
    await this.t.inMain(this.s().load).click();
    const st = this.t.inMain(this.s().status);
    await expect(st).not.toHaveText('');
    return (await st.innerText()).trim();
  }

  /** Idempotent: does nothing if already in the wanted state. Returns the final state. */
  async ensure(service: string, want: 'START' | 'STOP') {
    if ((await this.status(service)) === want) return want;
    await this.t.inMain(this.s().action).selectOption(want);
    await this.t.inMain(this.s().confirm).click();
    await expect(this.t.inMain(this.s().status)).toHaveText(want);
    return want;
  }
}
