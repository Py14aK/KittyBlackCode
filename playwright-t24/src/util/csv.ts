import { readFileSync } from 'node:fs';

/** Semicolon CSV (Xray importer convention), straight double quotes, UTF-8, optional BOM. */
export function readCsv(path: string, sep = ';'): Record<string, string>[] {
  const text = readFileSync(path, 'utf8').replace(/^﻿/, '');
  const rows: string[][] = [];
  let row: string[] = [], cell = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') q = false;
      else cell += c;
    } else if (c === '"') q = true;
    else if (c === sep) { row.push(cell); cell = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cell); if (row.some((x) => x !== '')) rows.push(row); row = []; cell = '';
    } else cell += c;
  }
  row.push(cell); if (row.some((x) => x !== '')) rows.push(row);
  const [head, ...body] = rows;
  if (!head) return [];
  return body.map((r) => Object.fromEntries(head.map((h, j) => [h.trim(), (r[j] ?? '').trim()])));
}
