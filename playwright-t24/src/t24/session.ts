import { expect, type FrameLocator, type Locator, type Page, type TestInfo } from '@playwright/test';
import { profile, type Action, type Profile } from './profiles';

export interface Credentials { user: string; pass: string }

export interface Messages { errors: string[]; overrides: string[]; complete: string | null }

/** Thin wrapper over one T24 Browser tab. Pages (POM) are built on top of this. */
export class T24 {
  readonly p: Profile;
  constructor(readonly page: Page, readonly info?: TestInfo, p?: Profile, readonly preferKeys = false) {
    this.p = p ?? profile();
  }

  // ---------- frames ----------
  private scope(frameSel: string | null): Page | FrameLocator {
    return frameSel ? this.page.frameLocator(frameSel) : this.page;
  }
  banner() { return this.scope(this.p.frames.banner); }
  main() { return this.scope(this.p.frames.main); }
  inMain(sel: string): Locator { return this.main().locator(sel); }

  // ---------- session ----------
  async login(c: Credentials) {
    if (!c.user || !c.pass) throw new Error('Credentials missing: set them in .env, never in code');
    await this.page.goto(process.env.T24_BASE_URL ?? '/');
    await this.page.locator(this.p.login.user).fill(c.user);
    await this.page.locator(this.p.login.pass).fill(c.pass);
    await this.page.locator(this.p.login.submit).click();
    await expect(this.banner().locator(this.p.commandLine)).toBeVisible();
  }
  async logout() {
    await this.banner().locator(this.p.signOff).click();
    await expect(this.page.locator(this.p.login.user)).toBeVisible();
  }

  /** Type a T24 command line string, e.g. "ENQ TXN.ENTRY" or "FT,VERSION A FT123". */
  async command(cmd: string) {
    const box = this.banner().locator(this.p.commandLine);
    await box.fill(cmd);
    if (this.p.commandGo) await this.banner().locator(this.p.commandGo).click();
    else await box.press('Enter');
  }

  // ---------- fields ----------
  field(name: string): Locator { return this.inMain(this.p.field(name)); }

  /** Fill and leave the field, so validation/enrichment routines (AUTH NEW CONTENT style) fire. */
  async set(name: string, value: string) {
    const f = this.field(name);
    await f.fill(value);
    await f.press('Tab');
  }
  async setMany(values: Record<string, string | undefined>) {
    for (const [k, v] of Object.entries(values)) if (v !== undefined && v !== '') await this.set(k, v);
  }
  async value(name: string) { return (await this.field(name).inputValue()).trim(); }

  /** Wait until a routine has populated a dependent field (e.g. CREDIT.ACCT.NO after CREDIT.CURRENCY). */
  async waitFilled(name: string) { await expect(this.field(name)).not.toHaveValue(''); }

  // ---------- actions ----------
  async act(a: Action) {
    const key = this.p.keys[a];
    if (this.preferKeys && key) {
      // Keyboard events go to the focused frame. After a command the focus sits in the banner
      // (command line), so move it into the work frame first or the F-key is silently lost.
      const body = this.inMain('body');
      await body.evaluate(() => window.focus());
      await body.press(key);
    }
    else await this.inMain(this.p.toolbar[a]).click();
  }

  async messages(): Promise<Messages> {
    const m = this.p.messages;
    const texts = async (s: string) => (await this.inMain(s).allInnerTexts()).map((t) => t.trim()).filter(Boolean);
    const complete = (await texts(m.complete))[0] ?? null;
    return { errors: await texts(m.error), overrides: await texts(m.override), complete };
  }

  /** Accept every override currently shown. Errors are never accepted: the caller decides. */
  async acceptOverrides() {
    const boxes = this.inMain(this.p.messages.overrideAccept);
    for (let i = 0; i < (await boxes.count()); i++) await boxes.nth(i).check();
  }

  /** Validate, accept overrides if allowed, commit, and return the record id from "Txn Complete". */
  async validateAndCommit(opts: { acceptOverrides?: boolean } = {}): Promise<{ id: string | null; msgs: Messages }> {
    await this.act('validate');
    let msgs = await this.messages();
    if (msgs.errors.length) return { id: null, msgs };
    if (msgs.overrides.length) {
      if (!opts.acceptOverrides) return { id: null, msgs };
      await this.acceptOverrides();
    }
    await this.act('commit');
    await expect(this.inMain(this.p.messages.complete).or(this.inMain(this.p.messages.error)).first()).toBeVisible();
    msgs = await this.messages();
    return { id: this.idFrom(msgs.complete), msgs };
  }

  idFrom(text: string | null) { return text?.match(this.p.completeRe)?.[1] ?? null; }

  // ---------- evidence ----------
  /** Screenshot attached to the HTML report and kept for Xray evidence. */
  async evidence(label: string) {
    const buf = await this.page.screenshot({ fullPage: true });
    await this.info?.attach(label, { body: buf, contentType: 'image/png' });
    return buf;
  }
}
