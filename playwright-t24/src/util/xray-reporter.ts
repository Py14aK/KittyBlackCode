/**
 * Playwright reporter -> Xray JSON execution import file.
 * Test key comes from a tag in the title, e.g.  test('FT outgoing EUR @TKT-00042', ...)
 * Flavour: XRAY_FLAVOUR=server (default, Server/DC: PASS/FAIL, "evidences")
 *          XRAY_FLAVOUR=cloud  (PASSED/FAILED, "evidence")
 * Format per Xray "Import Execution Results - Xray JSON" docs. Recheck field names against
 * your Xray version before the first real import (status: ASSUMED until one import succeeds).
 */
import type { Reporter, TestCase, TestResult, FullResult } from '@playwright/test/reporter';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const KEY = /@([A-Z][A-Z0-9]+-\d+)/;

export default class XrayReporter implements Reporter {
  private tests: any[] = [];
  private cloud = process.env.XRAY_FLAVOUR === 'cloud';
  private start = new Date();

  onTestEnd(test: TestCase, result: TestResult) {
    const key = test.title.match(KEY)?.[1] ?? test.tags.map((t) => t.match(KEY)?.[1]).find(Boolean);
    if (!key) return;                       // untagged tests are not reported to Xray
    const ok = result.status === 'passed';
    const ev = result.attachments
      .filter((a) => a.contentType === 'image/png')
      .map((a, i) => ({
        data: (a.body ?? (a.path ? readFileSync(a.path) : Buffer.alloc(0))).toString('base64'),
        filename: `${key}_${i + 1}_${a.name.replace(/[^\w.-]+/g, '_')}.png`,
        contentType: 'image/png',
      }));
    const err = result.errors.map((e) => e.message ?? '').join('\n').slice(0, 4000);
    this.tests.push({
      testKey: key,
      start: result.startTime.toISOString(),
      finish: new Date(result.startTime.getTime() + result.duration).toISOString(),
      status: this.cloud ? (ok ? 'PASSED' : 'FAILED') : (ok ? 'PASS' : 'FAIL'),
      comment: ok ? `Playwright: passed (${test.title})` : `Playwright: ${result.status}\n${err}`,
      [this.cloud ? 'evidence' : 'evidences']: ev,
    });
  }

  onEnd(_r: FullResult) {
    const day = new Date().toISOString().slice(0, 10);
    const out = {
      info: {
        summary: `Playwright run ${day} ${process.env.T24_RELEASE ?? ''} ${process.env.T24_TARGET ?? ''}`.trim(),
        startDate: this.start.toISOString(),
        finishDate: new Date().toISOString(),
      },
      tests: this.tests,
    };
    mkdirSync('reports', { recursive: true });
    const f = join('reports', `xray_execution_${day}.json`);
    writeFileSync(f, JSON.stringify(out, null, 2));
    console.log(`xray: ${this.tests.length} tagged results -> ${f}`);
  }
}
