import { existsSync, lstatSync, realpathSync, rmSync, symlinkSync } from 'node:fs';
import { copyFile, cp, mkdir, rm } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';

const here = dirname(fileURLToPath(import.meta.url));
const pipelineMode = process.env.ROADMAP_V2_PIPELINE_RENDER === '1';

function requiredEnv(name, fallback) {
  const value = process.env[name] || fallback;
  if (pipelineMode && !process.env[name]) {
    console.error(`Missing required roadmap-v2 renderer environment variable: ${name}`);
    process.exit(2);
  }
  return value;
}

const webRoot = resolve(requiredEnv('ROADMAP_RENDERER_DIR', join(here, '..')));
const outDir = resolve(requiredEnv('RENDER_OUTPUT_DIR', join(webRoot, 'dist')));
const workDir = resolve(requiredEnv('RENDER_WORK_DIR', `${outDir}.work`));
const nodeModules = resolve(requiredEnv('ROADMAP_V2_NODE_MODULES', join(webRoot, 'node_modules')));
const astroCacheDir = resolve(requiredEnv('ASTRO_CACHE_DIR', join(workDir, '.astro-cache')));
const viteCacheDir = resolve(requiredEnv('VITE_CACHE_DIR', join(workDir, '.vite-cache')));
const astroBin = join(nodeModules, 'astro', 'bin', 'astro.mjs');
const webAwesomeSource = join(nodeModules, '@awesome.me', 'webawesome', 'dist-cdn');
const webAwesomeTarget = join(outDir, 'vendor', 'webawesome', 'dist-cdn');

if (!existsSync(nodeModules)) {
  console.error(`Missing roadmap-v2 renderer node_modules at ${nodeModules}. Run the roadmap-v2 setup command first.`);
  process.exit(2);
}

if (!existsSync(astroBin)) {
  console.error(`Missing Astro runtime at ${astroBin}. Run the roadmap-v2 setup command first.`);
  process.exit(2);
}

if (!existsSync(webAwesomeSource)) {
  console.error(`Missing Web Awesome assets at ${webAwesomeSource}. Run the roadmap-v2 setup command first.`);
  process.exit(2);
}

await rm(workDir, { recursive: true, force: true });
await mkdir(workDir, { recursive: true });
await mkdir(join(workDir, 'public'), { recursive: true });

function ensureSymlink(name, target, type) {
  const link = join(workDir, name);
  if (existsSync(link)) {
    const stat = lstatSync(link);
    if (stat.isSymbolicLink() && realpathSync(link) === realpathSync(target)) {
      return;
    }
    rmSync(link, { recursive: true, force: true });
  }
  symlinkSync(target, link, type);
}

await copyFile(join(webRoot, 'astro.config.mjs'), join(workDir, 'astro.config.mjs'));
await copyFile(join(webRoot, 'package.json'), join(workDir, 'package.json'));
await copyFile(join(webRoot, 'tsconfig.json'), join(workDir, 'tsconfig.json'));
await cp(join(webRoot, 'src'), join(workDir, 'src'), { recursive: true, force: true });
ensureSymlink('node_modules', nodeModules, 'dir');

const env = {
  ...process.env,
  ASTRO_TELEMETRY_DISABLED: process.env.ASTRO_TELEMETRY_DISABLED || '1',
  ROADMAP_RENDERER_DIR: webRoot,
  ROADMAP_V2_NODE_MODULES: nodeModules,
  RENDER_OUTPUT_DIR: outDir,
  RENDER_WORK_DIR: workDir,
  ASTRO_CACHE_DIR: astroCacheDir,
  VITE_CACHE_DIR: viteCacheDir
};

const child = spawn(
  process.execPath,
  [astroBin, 'build'],
  {
    cwd: workDir,
    env,
    stdio: 'inherit'
  }
);

child.on('exit', (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  if ((code ?? 1) !== 0) {
    process.exit(code ?? 1);
    return;
  }
  rm(webAwesomeTarget, { recursive: true, force: true })
    .then(() => mkdir(dirname(webAwesomeTarget), { recursive: true }))
    .then(() => cp(webAwesomeSource, webAwesomeTarget, { recursive: true, force: true }))
    .then(() => process.exit(0))
    .catch((error) => {
      console.error(error);
      process.exit(1);
    });
});
