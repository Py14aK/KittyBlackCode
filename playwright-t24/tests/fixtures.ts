import { test as base, expect } from '@playwright/test';
import { T24, type Credentials } from '../src/t24/session';
import { FtPaymentPage } from '../src/pages/FtPaymentPage';
import { EnquiryPage } from '../src/pages/EnquiryPage';
import { ServicesPage } from '../src/pages/ServicesPage';

const env = (k: string, mockDefault: string) =>
  process.env[k] || (process.env.T24_TARGET === 'mock' ? mockDefault : '');

export const inputter: Credentials = { user: env('T24_INPUT_USER', 'INPUTTER1'), pass: env('T24_INPUT_PASS', 'x') };
export const authoriser: Credentials = { user: env('T24_AUTH_USER', 'AUTHORISER1'), pass: env('T24_AUTH_PASS', 'x') };

type F = { t24: T24; ft: FtPaymentPage; enq: EnquiryPage; ts: ServicesPage };

export const test = base.extend<F>({
  t24: async ({ page }, use, info) => { await use(new T24(page, info, undefined, process.env.T24_PREFER_KEYS === '1')); },
  ft: async ({ t24 }, use) => { await use(new FtPaymentPage(t24)); },
  enq: async ({ t24 }, use) => { await use(new EnquiryPage(t24)); },
  ts: async ({ t24 }, use) => { await use(new ServicesPage(t24)); },
});
export { expect };
