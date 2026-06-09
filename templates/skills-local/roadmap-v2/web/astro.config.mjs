import { join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const rendererDir = new URL('.', import.meta.url);
const pipelineMode = process.env.ROADMAP_V2_PIPELINE_RENDER === '1';

function requiredEnv(name, fallback) {
  const value = process.env[name] || fallback;
  if (pipelineMode && !process.env[name]) {
    throw new Error(`Missing required roadmap-v2 renderer environment variable: ${name}`);
  }
  return value;
}

const rendererPath = resolve(requiredEnv('ROADMAP_RENDERER_DIR', fileURLToPath(rendererDir)));
const outDir = resolve(requiredEnv('RENDER_OUTPUT_DIR', join(rendererPath, 'dist')));
const rootDir = resolve(requiredEnv('RENDER_WORK_DIR', `${outDir}.work`));
const astroCacheDir = resolve(requiredEnv('ASTRO_CACHE_DIR', join(rootDir, '.astro-cache')));
const viteCacheDir = resolve(requiredEnv('VITE_CACHE_DIR', join(rootDir, '.vite-cache')));
const publicDir = join(rootDir, 'public');

export default {
  root: rootDir,
  srcDir: join(rootDir, 'src'),
  publicDir,
  output: 'static',
  outDir,
  cacheDir: astroCacheDir,
  vite: {
    cacheDir: viteCacheDir
  },
  build: {
    format: 'file'
  }
};
