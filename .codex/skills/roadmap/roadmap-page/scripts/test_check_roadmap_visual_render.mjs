#!/usr/bin/env node
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const checkerPath = path.resolve(scriptDir, "check_roadmap_visual_render.mjs");

const darkCss = `
  :root {
    color-scheme: dark;
    --text: #e6e6e6;
    --muted: #a3a3a3;
    --border: #333333;
    --page: #191919;
    --surface: #202020;
    --soft: #242424;
    --soft-2: #2a2a2a;
    --accent: #6aaed6;
    --code: #e6e6e6;
    --code-bg: #2f3437;
    --pre-bg: #111111;
    --pre-text: #d4d4d4;
  }
  * { box-sizing: border-box; }
  body {
    color-scheme: dark;
    margin: 0;
    color: var(--text);
    background: var(--page);
    font-family: Arial, sans-serif;
    font-size: 18px;
    line-height: 1.55;
  }
  main {
    max-width: 960px;
    margin: 0 auto;
    padding: 32px 28px 56px;
  }
  p, ul, ol, .lead, .callout { max-width: none; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 22px;
    table-layout: fixed;
    background: var(--surface);
  }
  th, td {
    border: 1px solid var(--border);
    padding: 9px 10px;
    vertical-align: top;
    overflow-wrap: anywhere;
    background: var(--surface);
  }
  th {
    background: var(--soft-2);
    text-align: left;
    font-weight: 700;
  }
  code {
    color: var(--code);
    background: var(--code-bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 4px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 0.92em;
  }
  pre {
    margin: 12px 0 22px;
    padding: 14px 16px;
    color: var(--pre-text);
    background: var(--pre-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    overflow: auto;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 16px;
    line-height: 1.45;
    white-space: pre;
  }
  pre code {
    color: inherit;
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    font: inherit;
  }
  .syntax-key { color: #8cc7ff; font-weight: 700; }
  .syntax-op { color: #c8b6ff; }
  .syntax-value { color: #a8e6cf; }
  .syntax-comment { color: #a3a3a3; }
  .syntax-risk { color: #ffe27a; }
`;

const legacyLightCss = `
  :root {
    --text: #1f2937;
    --border: #cbd5e1;
    --page: #f8fafc;
    --surface: #ffffff;
    --soft-2: #e8eef6;
    --code: #0f172a;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    color: var(--text);
    background: var(--page);
    font-family: Arial, sans-serif;
    font-size: 18px;
    line-height: 1.55;
  }
  main {
    max-width: 960px;
    margin: 0 auto;
    padding: 32px 28px 56px;
  }
  p, ul, ol, .lead, .callout { max-width: none; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 22px;
    table-layout: fixed;
    background: var(--surface);
  }
  th, td {
    border: 1px solid var(--border);
    padding: 9px 10px;
    vertical-align: top;
    overflow-wrap: anywhere;
    background: var(--surface);
  }
  th { background: var(--soft-2); text-align: left; font-weight: 700; }
  code {
    color: var(--code);
    background: #edf2f7;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1px 4px;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 0.92em;
  }
  pre {
    margin: 12px 0 22px;
    padding: 14px 16px;
    color: #dbeafe;
    background: #111827;
    border-radius: 6px;
    overflow: auto;
    font-family: Consolas, Monaco, "Courier New", monospace;
    font-size: 16px;
    line-height: 1.45;
    white-space: pre;
  }
  pre code {
    color: inherit;
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    font: inherit;
  }
  .syntax-key { color: #93c5fd; font-weight: 700; }
  .syntax-op { color: #c4b5fd; }
  .syntax-value { color: #bbf7d0; }
`;

function htmlFor(codeBlock, { css = darkCss, themeMarker = true } = {}) {
  return `<!doctype html>
<html lang="pt-BR"${themeMarker ? ' data-visual-theme="notion-dark"' : ""}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Roadmap visual check fixture</title>
  <style>${css}</style>
</head>
<body>
  <main>
    <h1>Roadmap visual check fixture</h1>
    <p class="lead">Fixture used to verify rendered visual checks.</p>
    <p>This paragraph intentionally spans the useful content width.</p>
    <table>
      <tr><th>Fonte</th><th>Uso</th></tr>
      <tr><td>Documentacao</td><td>Validacao de superficie estruturada.</td></tr>
    </table>
    ${codeBlock}
  </main>
</body>
</html>
`;
}

function createRoadmapDir(name, codeBlock) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), `${name}-`));
  fs.writeFileSync(path.join(dir, "roadmap.html"), htmlFor(codeBlock), "utf-8");
  return dir;
}

function runChecker(dir) {
  const result = spawnSync(process.execPath, [checkerPath, "--html", path.join(dir, "roadmap.html")], {
    encoding: "utf-8",
  });
  const checksPath = path.join(dir, ".roadmap", "pipeline", "05-visual-render", "render-checks.json");
  assert.ok(
    fs.existsSync(checksPath),
    [
      `render-checks.json was not created for ${dir}`,
      `exit: ${result.status}`,
      `stdout: ${result.stdout}`,
      `stderr: ${result.stderr}`,
    ].join("\n"),
  );
  const checks = JSON.parse(fs.readFileSync(checksPath, "utf-8"));
  return { result, checks };
}

const missingHighlightDir = createRoadmapDir(
  "roadmap-highlight-fail",
  `<pre class="code-block language-cwl" aria-label="Consulta conceitual de Logs Insights"><code>fields route, status_code
| filter status_code >= 500
| stats count() by route</code></pre>`,
);
const missingHighlight = runChecker(missingHighlightDir);
assert.notEqual(missingHighlight.result.status, 0, "technical code without highlight must fail");
assert.equal(missingHighlight.checks.status, "falha");
assert.ok(missingHighlight.checks.failures.highlight.length > 0);
assert.deepEqual(missingHighlight.checks.failures.theme, []);

const highlightedDir = createRoadmapDir(
  "roadmap-highlight-pass",
  `<pre class="code-block language-cwl" aria-label="Consulta conceitual de Logs Insights"><code><span class="syntax-key">fields</span> <span class="syntax-value">route</span>, <span class="syntax-value">status_code</span>
<span class="syntax-op">|</span> <span class="syntax-key">filter</span> <span class="syntax-value">status_code</span> <span class="syntax-op">&gt;=</span> <span class="syntax-value">500</span>
<span class="syntax-op">|</span> <span class="syntax-key">stats</span> <span class="syntax-key">count</span><span class="syntax-op">()</span> <span class="syntax-key">by</span> <span class="syntax-value">route</span></code></pre>`,
);
const highlighted = runChecker(highlightedDir);
assert.equal(highlighted.result.status, 0, highlighted.result.stderr);
assert.equal(highlighted.checks.status, "passa");
assert.deepEqual(highlighted.checks.failures.theme, []);
assert.deepEqual(highlighted.checks.failures.highlight, []);
assert.deepEqual(highlighted.checks.failures.preCodeChip, []);

const legacyLightDir = createRoadmapDir(
  "roadmap-legacy-theme-fail",
  `<pre class="code-block language-cwl" aria-label="Consulta conceitual de Logs Insights"><code><span class="syntax-key">fields</span> <span class="syntax-value">route</span>, <span class="syntax-value">status_code</span>
<span class="syntax-op">|</span> <span class="syntax-key">filter</span> <span class="syntax-value">status_code</span> <span class="syntax-op">&gt;=</span> <span class="syntax-value">500</span>
<span class="syntax-op">|</span> <span class="syntax-key">stats</span> <span class="syntax-key">count</span><span class="syntax-op">()</span> <span class="syntax-key">by</span> <span class="syntax-value">route</span></code></pre>`,
);
fs.writeFileSync(
  path.join(legacyLightDir, "roadmap.html"),
  htmlFor(
    `<pre class="code-block language-cwl" aria-label="Consulta conceitual de Logs Insights"><code><span class="syntax-key">fields</span> <span class="syntax-value">route</span>, <span class="syntax-value">status_code</span>
<span class="syntax-op">|</span> <span class="syntax-key">filter</span> <span class="syntax-value">status_code</span> <span class="syntax-op">&gt;=</span> <span class="syntax-value">500</span>
<span class="syntax-op">|</span> <span class="syntax-key">stats</span> <span class="syntax-key">count</span><span class="syntax-op">()</span> <span class="syntax-key">by</span> <span class="syntax-value">route</span></code></pre>`,
    { css: legacyLightCss, themeMarker: false },
  ),
  "utf-8",
);
const legacyLight = runChecker(legacyLightDir);
assert.notEqual(legacyLight.result.status, 0, "legacy light theme must fail");
assert.equal(legacyLight.checks.status, "falha");
assert.ok(legacyLight.checks.failures.theme.length > 0);

console.log("passa: testes do render visual do roadmap validam tema, highlight e pre code");
