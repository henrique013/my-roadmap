import { mkdir, writeFile } from 'node:fs/promises';
import { createRequire } from 'node:module';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const htmlPath = process.argv[2];
const outputDir = process.argv[3];

if (!htmlPath || !outputDir) {
  console.error('Usage: node scripts/check-visual.mjs <html-path> <output-dir>');
  process.exit(2);
}

function loadPlaywright() {
  const nodeModules = process.env.ROADMAP_V2_NODE_MODULES;
  const requireFrom = nodeModules
    ? createRequire(join(nodeModules, '.roadmap-v2-runtime.cjs'))
    : createRequire(import.meta.url);
  return requireFrom('playwright');
}

const { chromium } = loadPlaywright();
const strictVisual = process.env.ROADMAP_V2_VISUAL_STRICT !== '0';

await mkdir(outputDir, { recursive: true });

const viewports = [
  { name: 'desktop', width: 1366, height: 900 },
  { name: 'mobile', width: 390, height: 844 }
];
const checks = [];
let browser;

try {
  browser = await chromium.launch({
    chromiumSandbox: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
} catch (error) {
  checks.push({
    viewport: 'all',
    status: 'skipped',
    reason: 'browser-launch-failed',
    error: String(error)
  });
  await writeFile(`${outputDir}/checks.json`, JSON.stringify({ checks }, null, 2) + '\n', 'utf-8');
  process.exit(strictVisual ? 1 : 0);
}

try {
  for (const viewport of viewports) {
    const page = await browser.newPage({ viewport });
    await page.route('**/*', (route) => {
      const url = route.request().url();
      if (url.startsWith('http://') || url.startsWith('https://')) {
        route.abort();
        return;
      }
      route.continue();
    });
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });
    const metrics = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      textLength: document.body.innerText.trim().length
    }));
    const screenshot = `${outputDir}/${viewport.name}.png`;
    await page.screenshot({ path: screenshot, fullPage: true });
    const status = metrics.scrollWidth <= metrics.clientWidth + 2 && metrics.textLength > 40 ? 'ok' : 'failed';
    checks.push({ viewport: viewport.name, status, metrics, screenshot });
    await page.close();
  }
} finally {
  if (browser) {
    await browser.close();
  }
}

await writeFile(`${outputDir}/checks.json`, JSON.stringify({ checks }, null, 2) + '\n', 'utf-8');

if (checks.some((check) => check.status !== 'ok')) {
  process.exit(1);
}
