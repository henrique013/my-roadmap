import { cp, mkdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const webRoot = resolve(join(here, '..'));
const nodeModules = resolve(process.env.ROADMAP_V2_NODE_MODULES || join(webRoot, 'node_modules'));
const outputDir = process.env.RENDER_OUTPUT_DIR;

if (!outputDir) {
  console.error('RENDER_OUTPUT_DIR is required. Web Awesome assets are output artifacts, not files under web/public.');
  process.exit(2);
}

const source = join(nodeModules, '@awesome.me', 'webawesome', 'dist-cdn');
const target = join(resolve(outputDir), 'vendor', 'webawesome', 'dist-cdn');

await mkdir(dirname(target), { recursive: true });
await cp(source, target, { recursive: true, force: true });
