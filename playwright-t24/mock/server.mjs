// Offline T24 Browser look-alike for developing and self-testing the harness.
// It imitates structure (login, framed command line, transaction screen, enquiry,
// TS services, H table, base64 XML), NOT Temenos code. Behaviour is invented
// where marked ASSUMED in mock/README.md. Run: node mock/server.mjs [port]
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const port = Number(process.argv[2] ?? process.env.MOCK_PORT ?? 4824);
const routes = {
  '/': 'login.html',
  '/BrowserWeb/servlet/BrowserServlet': 'login.html',
  '/home': 'home.html',
  '/frame/banner': 'banner.html',
  '/frame/work': 'work.html',
};
const types = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript' };

http
  .createServer(async (req, res) => {
    const path = new URL(req.url ?? '/', 'http://x').pathname;
    const file = routes[path] ?? path.replace(/^\/+/, '');
    if (file.includes('..')) { res.writeHead(400).end(); return; }
    try {
      const body = await readFile(join(root, file));
      res.writeHead(200, { 'content-type': types[extname(file)] ?? 'text/plain' }).end(body);
    } catch {
      res.writeHead(404).end('not found');
    }
  })
  .listen(port, () => console.log(`t24 mock on http://localhost:${port}`));
