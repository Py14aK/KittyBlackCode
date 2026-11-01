/**
 * Selector profiles. THE ONLY FILE TO EDIT WHEN THE REAL SCREEN DIFFERS.
 *
 * Status of each value:
 *   mock  = matches mock/ exactly (verified by the self-test suite)
 *   R21 / R26 = ASSUMED from general T24 Browser knowledge. Not yet checked on SYT.
 *   Verify on SYT with:  npx playwright codegen --channel=msedge --ignore-https-errors <url>
 *   then overwrite the value and delete its "ASSUMED" comment.
 */
export type Action = 'validate' | 'commit' | 'authorise';

export interface Profile {
  login: { user: string; pass: string; submit: string; error: string };
  /** iframe CSS selector, or null when the element lives on the top page / a popup window */
  frames: { banner: string | null; main: string | null };
  commandLine: string;
  commandGo: string | null;            // null: press Enter
  signOff: string;
  field: (name: string) => string;     // T24 field name verbatim, e.g. DEBIT.ACCT.NO
  toolbar: Record<Action, string>;
  keys: Partial<Record<Action, string>>; // F-key shortcuts, used when preferKeys=true
  messages: { error: string; override: string; overrideAccept: string; complete: string };
  completeRe: RegExp;                  // pulls the record id out of the completion message
  recordStatus: string;
  enquiry: { run: string; results: string };
  services: { name: string; load: string; status: string; action: string; confirm: string };
}

const mock: Profile = {
  login: { user: '[name="signOnName"]', pass: '[name="password"]', submit: '#sign-in', error: '#loginError' },
  frames: { banner: 'iframe[name="banner"]', main: 'iframe[name="main"]' },
  commandLine: '#commandValue',
  commandGo: '#cmdGo',
  signOff: '#signOff',
  field: (n) => `[id="fieldName:${n}"]`,
  toolbar: {
    validate: '[title="Validate a deal"]',
    commit: '[title="Commit the deal"]',
    authorise: '[title="Authorises a deal"]',
  },
  keys: { validate: 'F5', commit: 'F2', authorise: 'F9' },
  messages: { error: '#messages .error', override: '#messages .override', overrideAccept: '#messages .override input[type=checkbox]', complete: '#messages .complete' },
  completeRe: /Txn Complete:\s*(\S+)/,
  recordStatus: '#recordStatus',
  enquiry: { run: '[title="Run enquiry"]', results: '#enqResults' },
  services: { name: '[id="fieldName:SERVICE.NAME"]', load: '[title="Load"]', status: '#serviceStatus', action: '#serviceAction', confirm: '[title="Confirm"]' },
};

// ASSUMED: real T24 Browser keeps the same naming idioms (signOnName, fieldName:X,
// "Validate a deal" / "Commit the deal" toolbar titles, "Txn Complete:"). Frames and
// message containers differ by release and skin. Start from mock and correct per release.
const R21: Profile = { ...mock, keys: {} };   // keys unknown until checked: use toolbar clicks
const R26: Profile = { ...mock, keys: {} };

export const PROFILES: Record<string, Profile> = { mock, R21, R26 };

export function profile(): Profile {
  const key = process.env.T24_TARGET === 'mock' ? 'mock' : (process.env.T24_RELEASE ?? 'R21');
  const p = PROFILES[key];
  if (!p) throw new Error(`Unknown T24 profile "${key}". Known: ${Object.keys(PROFILES).join(', ')}`);
  return p;
}
