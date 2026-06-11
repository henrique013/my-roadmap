#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";

import { chromium } from "playwright";

const VIEWPORTS = [
  { name: "desktop", width: 1280, height: 900, isMobile: false },
  { name: "mobile", width: 390, height: 844, isMobile: true },
];

function usage() {
  return [
    "Uso:",
    "  docker/runtime/run node <skill-dir>/roadmap-page/scripts/check_roadmap_visual_render.mjs --html <roadmap-dir>/roadmap.html",
    "  docker/runtime/run node <skill-dir>/roadmap-page/scripts/check_roadmap_visual_render.mjs --roadmap-dir <roadmap-dir>",
  ].join("\n");
}

function parseArgs(argv) {
  const parsed = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) {
      throw new Error(`argumento inesperado: ${arg}`);
    }
    const key = arg.slice(2);
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`valor ausente para --${key}`);
    }
    parsed[key] = value;
    index += 1;
  }

  if (Boolean(parsed.html) === Boolean(parsed["roadmap-dir"])) {
    throw new Error("informe exatamente um entre --html e --roadmap-dir");
  }
  return parsed;
}

function isInside(child, parent) {
  const relative = path.relative(parent, child);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function assertInside(child, parent, label) {
  if (!isInside(child, parent)) {
    throw new Error(`${label} fora do diretório permitido: ${child}`);
  }
}

function resolveTargets(args) {
  const roadmapDir = path.resolve(args["roadmap-dir"] || path.dirname(path.resolve(args.html)));
  const htmlPath = path.resolve(args.html || path.join(roadmapDir, "roadmap.html"));
  if (path.basename(htmlPath) !== "roadmap.html") {
    throw new Error("--html deve apontar para roadmap.html");
  }
  if (!fs.existsSync(roadmapDir) || !fs.statSync(roadmapDir).isDirectory()) {
    throw new Error(`roadmap dir não existe: ${roadmapDir}`);
  }
  if (!fs.existsSync(htmlPath) || !fs.statSync(htmlPath).isFile()) {
    throw new Error(`roadmap.html ausente: ${htmlPath}`);
  }
  assertInside(htmlPath, roadmapDir, "roadmap.html");

  const internalDir = path.resolve(roadmapDir, ".roadmap");
  const visualPipeDir = path.resolve(internalDir, "pipeline", "05-visual-render");
  const playwrightDir = path.resolve(visualPipeDir, "playwright");
  assertInside(internalDir, roadmapDir, ".roadmap");
  assertInside(visualPipeDir, internalDir, ".roadmap/pipeline/05-visual-render");
  assertInside(playwrightDir, visualPipeDir, ".roadmap/pipeline/05-visual-render/playwright");

  return {
    roadmapDir,
    htmlPath,
    internalDir,
    visualPipeDir,
    playwrightDir,
    visualAuditPath: path.resolve(visualPipeDir, "visual-audit.md"),
    renderChecksPath: path.resolve(visualPipeDir, "render-checks.json"),
  };
}

function colorAlpha(value) {
  if (!value || value === "transparent") {
    return 0;
  }
  const match = String(value).match(/rgba?\(([^)]+)\)/i);
  if (!match) {
    return 1;
  }
  const parts = match[1].split(/[,\s/]+/).filter(Boolean);
  if (parts.length < 4) {
    return 1;
  }
  const alpha = Number.parseFloat(parts[3]);
  return Number.isFinite(alpha) ? alpha : 1;
}

function parseRgbColor(value) {
  if (!value || value === "transparent") {
    return null;
  }
  const match = String(value).match(/rgba?\(([^)]+)\)/i);
  if (!match) {
    return null;
  }
  const parts = match[1].split(/[,\s/]+/).filter(Boolean);
  if (parts.length < 3) {
    return null;
  }
  const rgb = parts.slice(0, 3).map((part) => Number.parseFloat(part));
  const alpha = parts.length >= 4 ? Number.parseFloat(parts[3]) : 1;
  if (rgb.some((part) => !Number.isFinite(part))) {
    return null;
  }
  return { r: rgb[0], g: rgb[1], b: rgb[2], a: Number.isFinite(alpha) ? alpha : 1 };
}

function relativeLuminance(color) {
  const values = [color.r, color.g, color.b].map((value) => {
    const channel = value / 255;
    return channel <= 0.03928
      ? channel / 12.92
      : ((channel + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2];
}

function isDarkSurface(value) {
  const parsed = parseRgbColor(value);
  return Boolean(parsed && parsed.a > 0.01 && relativeLuminance(parsed) <= 0.18);
}

function pxNumber(value) {
  const parsed = Number.parseFloat(String(value || "0"));
  return Number.isFinite(parsed) ? parsed : 0;
}

function hasPositiveBoxValue(values) {
  return values.some((value) => pxNumber(value) > 0.1);
}

function preCodeChipFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    for (const block of result.preCodeStyles) {
      const hasBackground = colorAlpha(block.backgroundColor) > 0.01;
      const hasBorder = hasPositiveBoxValue(block.borderWidths);
      const hasPadding = hasPositiveBoxValue(block.paddings);
      const hasRadius = hasPositiveBoxValue(block.borderRadii);

      if (hasBackground || hasBorder || hasPadding || hasRadius) {
        failures.push({
          viewport: result.viewport.name,
          index: block.index,
          text: block.text,
          reason: [
            hasBackground ? `background ${block.backgroundColor}` : null,
            hasBorder ? `border ${block.borderWidths.join(" ")}` : null,
            hasPadding ? `padding ${block.paddings.join(" ")}` : null,
            hasRadius ? `border-radius ${block.borderRadii.join(" ")}` : null,
          ].filter(Boolean).join(", "),
        });
      }
    }
  }

  return failures;
}

function highlightFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    for (const block of result.preBlocks) {
      if (
        block.hasCode &&
        block.looksTechnical &&
        !block.isConceptualVisual &&
        !block.hasHighlight
      ) {
        failures.push({
          viewport: result.viewport.name,
          index: block.index,
          text: block.text,
        });
      }
    }
  }

  return failures;
}

function darkThemeFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    if (result.theme.marker !== "notion-dark") {
      failures.push({
        viewport: result.viewport.name,
        check: "marker",
        expected: "notion-dark",
        actual: result.theme.marker || "(ausente)",
      });
    }
    if (!/\bdark\b/i.test(result.theme.colorScheme || "")) {
      failures.push({
        viewport: result.viewport.name,
        check: "color-scheme",
        expected: "dark",
        actual: result.theme.colorScheme || "(ausente)",
      });
    }
    for (const sample of result.theme.surfaceSamples) {
      if (!isDarkSurface(sample.backgroundColor)) {
        failures.push({
          viewport: result.viewport.name,
          check: "dark-surface",
          selector: sample.selector,
          index: sample.index,
          text: sample.text,
          backgroundColor: sample.backgroundColor,
        });
      }
    }
  }

  return failures;
}

async function collectRenderData(page) {
  return page.evaluate(() => {
    function parseColor(value) {
      if (!value || value === "transparent") {
        return { r: 0, g: 0, b: 0, a: 0 };
      }
      const match = value.match(/rgba?\(([^)]+)\)/i);
      if (!match) {
        return null;
      }
      const parts = match[1].split(/[,\s/]+/).filter(Boolean);
      const rgb = parts.slice(0, 3).map((part) => Number.parseFloat(part));
      const alpha = parts.length >= 4 ? Number.parseFloat(parts[3]) : 1;
      if (rgb.length < 3 || rgb.some((part) => !Number.isFinite(part))) {
        return null;
      }
      return { r: rgb[0], g: rgb[1], b: rgb[2], a: Number.isFinite(alpha) ? alpha : 1 };
    }

    function luminance(color) {
      const values = [color.r, color.g, color.b].map((value) => {
        const channel = value / 255;
        return channel <= 0.03928
          ? channel / 12.92
          : ((channel + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2];
    }

    function contrastRatio(foreground, background) {
      const foregroundColor = parseColor(foreground);
      const backgroundColor = parseColor(background);
      if (!foregroundColor || !backgroundColor) {
        return null;
      }
      const light = Math.max(luminance(foregroundColor), luminance(backgroundColor));
      const dark = Math.min(luminance(foregroundColor), luminance(backgroundColor));
      return Number(((light + 0.05) / (dark + 0.05)).toFixed(2));
    }

    function isDarkSurface(background) {
      const parsed = parseColor(background);
      return Boolean(parsed && parsed.a > 0.01 && luminance(parsed) <= 0.18);
    }

    function isVisible(element) {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
    }

    function isConceptualVisualPre(pre, text) {
      const markers = [
        pre.className,
        pre.getAttribute("aria-label") || "",
        pre.getAttribute("role") || "",
      ].join(" ").toLowerCase();
      const markedAsVisual = /(diagram|diagrama|fluxo|flow|ascii|timeline|linha-do-tempo|topology|topologia|state|estado|lane|progress|progresso|antes|depois|before|after)/.test(markers);
      const arrowFlow = /(?:->|=>|-->|<--|\|)/.test(text) && !/[=;{}[\]:]/.test(text);
      return markedAsVisual || arrowFlow;
    }

    function hasHighlightClass(element) {
      return Array.from(element.querySelectorAll("*")).some((child) =>
        Array.from(child.classList).some(
          (className) =>
            className.startsWith("syntax-") ||
            className.startsWith("token") ||
            className.startsWith("hljs-"),
        ),
      );
    }

    function looksTechnical(text) {
      const trimmed = text.trim();
      return (
        /[=;{}[\]:]/.test(trimmed) ||
        /^\s*[\w.-]+\s+\S+/m.test(trimmed) ||
        /<[^>]+>/.test(trimmed)
      );
    }

    function summarizeStyle(element, index) {
      const style = window.getComputedStyle(element);
      return {
        index,
        text: element.textContent.trim().slice(0, 120),
        color: style.color,
        backgroundColor: style.backgroundColor,
        borderWidths: [
          style.borderTopWidth,
          style.borderRightWidth,
          style.borderBottomWidth,
          style.borderLeftWidth,
        ],
        paddings: [
          style.paddingTop,
          style.paddingRight,
          style.paddingBottom,
          style.paddingLeft,
        ],
        borderRadii: [
          style.borderTopLeftRadius,
          style.borderTopRightRadius,
          style.borderBottomRightRadius,
          style.borderBottomLeftRadius,
        ],
        fontFamily: style.fontFamily,
        fontSize: style.fontSize,
      };
    }

    function effectiveBackground(element) {
      let current = element;
      while (current && current.nodeType === Node.ELEMENT_NODE) {
        const backgroundColor = window.getComputedStyle(current).backgroundColor;
        const parsed = parseColor(backgroundColor);
        if (parsed && parsed.a > 0.01) {
          return backgroundColor;
        }
        current = current.parentElement;
      }
      return "rgb(255, 255, 255)";
    }

    const documentElement = document.documentElement;
    const body = document.body;
    const themeSurfaceSelectors = [
      ["body", "body"],
      ["main", "main"],
      [".card", ".card"],
      [".callout", ".callout"],
      [".timeline-step", ".timeline-step"],
      [".flow-step", ".flow-step"],
      [".flow-steps span", ".flow-steps span"],
      [".step", ".step"],
      [".risk-step", ".risk-step"],
      [".position-strip", ".position-strip"],
      [".contract-map", ".contract-map"],
      [".visual-block", ".visual-block"],
      [".content-grid", ".content-grid"],
      [".state-card", ".state-card"],
      [".stream-card", ".stream-card"],
      [".event-card", ".event-card"],
      [".group-card", ".group-card"],
      [".tool-card", ".tool-card"],
      [".part", ".part"],
      [".group-shell", ".group-shell"],
      [".umbrella-map", ".umbrella-map"],
      [".topology-node", ".topology-node"],
      [".lane", ".lane"],
      [".node-list a", ".node-list a"],
      [".node-list .node-list-item", ".node-list .node-list-item"],
      [".process-card", ".process-card"],
      [".visual-card", ".visual-card"],
      [".concept-card", ".concept-card"],
      [".path-card", ".path-card"],
      [".decision-card", ".decision-card"],
      [".stage", ".stage"],
      [".segment", ".segment"],
      [".panel", ".panel"],
      [".box", ".box"],
      [".map-card", ".map-card"],
      [".layer", ".layer"],
      [".node-card", ".node-card"],
      [".mini-card", ".mini-card"],
      [".boundary-card", ".boundary-card"],
      [".handoff-card", ".handoff-card"],
      [".flow-mini > *", ".flow-mini > *"],
      ["th", "th"],
      ["td", "td"],
      ["code:not(pre code)", "inline code"],
      ["pre", "pre"],
      [".tag", ".tag"],
    ];
    const themeSurfaceSamples = themeSurfaceSelectors.flatMap(([selector, label]) =>
      Array.from(document.querySelectorAll(selector))
        .filter(isVisible)
        .slice(0, 8)
        .map((element, index) => {
          const backgroundColor = effectiveBackground(element);
          return {
            selector: label,
            index,
            text: element.textContent.trim().slice(0, 80),
            backgroundColor,
            isDark: isDarkSurface(backgroundColor),
          };
        }),
    );
    const clientWidth = documentElement.clientWidth;
    const scrollWidth = Math.max(documentElement.scrollWidth, body ? body.scrollWidth : 0);
    const main = document.querySelector("main");
    const mainRect = main ? main.getBoundingClientRect() : null;
    const mainWidth = mainRect ? mainRect.width : 0;

    const contentElements = Array.from(
      document.querySelectorAll("main p, main ul, main ol, main .lead, main .callout"),
    ).filter((element) => {
      if (!isVisible(element)) {
        return false;
      }
      if (
        element.closest(
          ".card, table, pre, .tag, .small, .step, .risk-step, .position-strip, .contract-map, .visual-block, .content-grid, .timeline, .timeline-step, .flow-steps, .flow-step, .state-grid, .state-card, .topology, .topology-node, .lane-map, .lane, .node-list, .stream-card, .event-card, .group-card, .tool-card, .part, .group-shell, .umbrella-map, .process-card, .visual-card, .concept-card, .path-card, .decision-card, .stage, .segment, .panel, .box, .map-card, .layer, .node-card, .mini-card, .boundary-card, .handoff-card, .flow-mini",
        )
      ) {
        return false;
      }
      return true;
    });

    const contentWidths = contentElements.map((element, index) => {
      const rect = element.getBoundingClientRect();
      return {
        index,
        selector: element.matches(".callout")
          ? ".callout"
          : element.matches(".lead")
            ? ".lead"
            : element.tagName.toLowerCase(),
        text: element.textContent.trim().slice(0, 120),
        width: Number(rect.width.toFixed(2)),
        mainWidth: Number(mainWidth.toFixed(2)),
        ratio: mainWidth > 0 ? Number((rect.width / mainWidth).toFixed(3)) : 0,
      };
    });

    const contrastSamples = [];
    const sampleSelectors = [
      ["body", "body"],
      ["p", "parágrafo"],
      ["a", "link"],
      ["code:not(pre code)", "inline code"],
      ["pre", "bloco de código"],
      [".tag", "tag"],
      [".small", "texto auxiliar"],
      [".route-label", "route-label"],
      [".node-list a", "node-list"],
      [
        ".flow-step, .step, .state-card, .stream-card, .event-card, .group-card, .tool-card, .part, .handoff-card, .lane, .boundary-card",
        "visual customizado",
      ],
    ];
    for (const [selector, label] of sampleSelectors) {
      const elements = Array.from(document.querySelectorAll(selector)).filter(isVisible).slice(0, 8);
      for (const element of elements) {
        const style = window.getComputedStyle(element);
        const backgroundColor = effectiveBackground(element);
        contrastSamples.push({
          label,
          text: element.textContent.trim().slice(0, 80),
          color: style.color,
          backgroundColor,
          ratio: contrastRatio(style.color, backgroundColor),
        });
      }
    }

    const preBlocks = Array.from(document.querySelectorAll("pre")).map((pre, index) => {
      const text = pre.textContent.trim();
      return {
        index,
        text: text.slice(0, 160),
        hasCode: Boolean(pre.querySelector("code")),
        hasHighlight: hasHighlightClass(pre),
        isConceptualVisual: isConceptualVisualPre(pre, text),
        hasAsciiException: pre.getAttribute("data-ascii-exception") === "true",
        asciiReason: pre.getAttribute("data-ascii-reason") || "",
        looksTechnical: looksTechnical(text),
        className: pre.className,
        ariaLabel: pre.getAttribute("aria-label") || "",
      };
    });

    const preCodeStyles = Array.from(document.querySelectorAll("pre code")).map(
      (element, index) => summarizeStyle(element, index),
    );

    return {
      title: document.title,
      theme: {
        marker: documentElement.getAttribute("data-visual-theme") || "",
        colorScheme: window.getComputedStyle(documentElement).colorScheme || window.getComputedStyle(body).colorScheme || "",
        surfaceSamples: themeSurfaceSamples,
      },
      overflow: {
        clientWidth,
        scrollWidth,
        hasGlobalOverflow: scrollWidth > clientWidth + 1,
      },
      contentWidths,
      contrastSamples,
      preBlocks,
      preCodeStyles,
    };
  });
}

async function renderViewport(browser, targets, viewport, externalRequests) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    deviceScaleFactor: 1,
    isMobile: viewport.isMobile,
  });

  await context.route("**/*", async (route) => {
    const requestUrl = route.request().url();
    if (/^https?:\/\//i.test(requestUrl)) {
      externalRequests.push(requestUrl);
      await route.abort("blockedbyclient");
      return;
    }
    await route.continue();
  });

  const page = await context.newPage();
  await page.goto(pathToFileURL(targets.htmlPath).href, { waitUntil: "load" });
  await page.waitForLoadState("networkidle").catch(() => {});
  await page.waitForTimeout(100);

  const screenshotPath = path.resolve(targets.playwrightDir, `${viewport.name}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });
  const data = await collectRenderData(page);
  await context.close();
  return { viewport, screenshotPath, ...data };
}

function overflowFailures(renderResults) {
  return renderResults
    .filter((result) => result.overflow.hasGlobalOverflow)
    .map((result) => ({
      viewport: result.viewport.name,
      clientWidth: result.overflow.clientWidth,
      scrollWidth: result.overflow.scrollWidth,
    }));
}

function contentWidthFailures(renderResults) {
  const failures = [];
  for (const result of renderResults) {
    if (result.viewport.name !== "desktop") {
      continue;
    }
    for (const item of result.contentWidths) {
      if (item.mainWidth >= 900 && item.ratio < 0.9) {
        failures.push({ viewport: result.viewport.name, ...item });
      }
    }
  }
  return failures;
}

function contrastFailures(renderResults) {
  const failures = [];
  for (const result of renderResults) {
    for (const sample of result.contrastSamples) {
      if (sample.ratio !== null && sample.ratio < 4.5 && colorAlpha(sample.color) > 0.01) {
        failures.push({ viewport: result.viewport.name, ...sample });
      }
    }
  }
  return failures;
}

function externalRequestFailures(externalRequests) {
  return [...new Set(externalRequests)].map((url) => ({ url }));
}

function conceptualPreFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    for (const block of result.preBlocks) {
      if (!block.isConceptualVisual) {
        continue;
      }
      if (block.hasAsciiException && block.asciiReason.trim()) {
        continue;
      }
      failures.push({
        viewport: result.viewport.name,
        index: block.index,
        text: block.text,
        className: block.className,
        ariaLabel: block.ariaLabel,
        reason: block.hasAsciiException
          ? "data-ascii-reason ausente ou vazio"
          : "visual conceitual em <pre> sem data-ascii-exception=\"true\"",
      });
    }
  }

  return failures;
}

function writeAudit(targets, renderResults, groupedFailures) {
  const failures = Object.values(groupedFailures).flat();
  const status = failures.length === 0 ? "passa" : "falha";
  const screenshotRows = renderResults.map((result) => {
    const relative = path.relative(targets.roadmapDir, result.screenshotPath);
    const note = result.overflow.hasGlobalOverflow
      ? `overflow global: ${result.overflow.scrollWidth}px para ${result.overflow.clientWidth}px`
      : "screenshot gerada";
    return `| ${result.viewport.name} | \`${relative}\` | ${note} |`;
  });

  const widthEvidence = groupedFailures.contentWidth.length === 0
    ? "parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop"
    : `${groupedFailures.contentWidth.length} bloco(s) estreito(s)`;
  const calloutFailure = groupedFailures.contentWidth.some((item) => item.selector === ".callout");
  const paragraphFailure = groupedFailures.contentWidth.some((item) => ["p", "ul", "ol", ".lead"].includes(item.selector));
  const tableThemeFailure = groupedFailures.theme.some((item) => ["th", "td"].includes(item.selector));

  const failureText = [];
  for (const item of groupedFailures.theme) {
    failureText.push(
      "### Tema visual `notion-dark` inválido",
      "",
      `- Onde apareceu: viewport ${item.viewport}${item.selector ? `, seletor ${item.selector}` : ""}.`,
      item.check === "dark-surface"
        ? `- Por que falha: superfície ${item.backgroundColor} não é escura o suficiente.`
        : `- Por que falha: ${item.check} atual \`${item.actual}\`; esperado \`${item.expected}\`.`,
      "- Revisão obrigatória: aplicar `data-visual-theme=\"notion-dark\"`, `color-scheme: dark` e os tokens escuros do sistema visual.",
      item.text ? `- Trecho: \`${item.text}\`` : "",
      "",
    );
  }
  for (const item of groupedFailures.contentWidth) {
    failureText.push(
      `### Bloco textual estreito ${item.index}`,
      "",
      `- Onde apareceu: viewport ${item.viewport}, seletor ${item.selector}.`,
      `- Por que falha: largura ${item.width}px para main ${item.mainWidth}px (${item.ratio}).`,
      "- Revisão obrigatória: remover max-width local ou reduzir a largura estrutural de `main`.",
      `- Trecho: \`${item.text}\``,
      "",
    );
  }
  for (const item of groupedFailures.overflow) {
    failureText.push(
      `### Overflow horizontal global em ${item.viewport}`,
      "",
      `- Por que falha: scrollWidth ${item.scrollWidth}px excede clientWidth ${item.clientWidth}px.`,
      "- Revisão obrigatória: corrigir largura, tabela, visual ou bloco que vaza do viewport.",
      "",
    );
  }
  for (const item of groupedFailures.contrast) {
    failureText.push(
      `### Contraste insuficiente em ${item.viewport}`,
      "",
      `- Onde apareceu: ${item.label}.`,
      `- Por que falha: contraste ${item.ratio}:1 entre ${item.color} e ${item.backgroundColor}.`,
      `- Trecho: \`${item.text}\``,
      "",
    );
  }
  for (const item of groupedFailures.externalRequests) {
    failureText.push(
      "### Asset externo bloqueado",
      "",
      `- Onde apareceu: ${item.url}.`,
      "- Revisão obrigatória: remover dependência remota ou incorporar alternativa local/autocontida.",
      "",
    );
  }
  for (const item of groupedFailures.preCodeChip) {
    failureText.push(
      "### `pre code` com estilo de chip",
      "",
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      `- Por que falha: ${item.reason}.`,
      "- Revisão obrigatória: defina `pre code` com fundo transparente, borda 0, padding 0 e `font: inherit`.",
      `- Trecho: \`${item.text}\``,
      "",
    );
  }
  for (const item of groupedFailures.highlight) {
    failureText.push(
      "### Snippet técnico sem highlight",
      "",
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      "- Por que falha: snippet técnico precisa de destaque semântico mínimo.",
      "- Revisão obrigatória: adicionar spans/classes `syntax-*` ou justificar como texto literal excepcional.",
      `- Trecho: \`${item.text}\``,
      "",
    );
  }
  for (const item of groupedFailures.conceptualPre) {
    failureText.push(
      "### Visual conceitual em `<pre>`",
      "",
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      `- Por que falha: ${item.reason}.`,
      "- Revisão obrigatória: trocar por componente HTML/CSS ou declarar exceção ASCII com `data-ascii-exception=\"true\"` e `data-ascii-reason`.",
      `- Classe: \`${item.className || "(sem classe)"}\``,
      `- Aria-label: \`${item.ariaLabel || "(sem aria-label)"}\``,
      `- Trecho: \`${item.text}\``,
      "",
    );
  }

  const renderChecksRelative = path.relative(targets.roadmapDir, targets.renderChecksPath);
  const audit = [
    "# Roadmap visual render audit",
    "",
    "## Metadados",
    "",
    `- Roadmap: ${path.basename(targets.roadmapDir)}`,
    "- Rodada: gerada pelo script Playwright",
    `- Data: ${new Date().toISOString()}`,
    `- HTML auditado: \`${path.relative(targets.roadmapDir, targets.htmlPath)}\``,
    "- Ferramenta: Playwright Library",
    "- Browser: Chromium headless",
    `- Viewports: ${VIEWPORTS.map((viewport) => `${viewport.name} ${viewport.width}x${viewport.height}`).join(", ")}`,
    `- Checks detalhados: \`${renderChecksRelative}\``,
    "",
    "## Evidências",
    "",
    "| Viewport | Screenshot | Observações |",
    "|---|---|---|",
    ...screenshotRows,
    "",
    "## Status geral",
    "",
    `Status geral: ${status}`,
    "",
    "## Checks mecânicos",
    "",
    "| Check | Status | Evidência |",
    "|---|---|---|",
    `| tema visual \`notion-dark\` aplicado | ${groupedFailures.theme.length === 0 ? "passa" : "falha"} | ${groupedFailures.theme.length === 0 ? "marcador, color-scheme e superfícies escuras confirmados" : `${groupedFailures.theme.length} problema(s) de tema`} |`,
    `| \`pre code\` não herda chip de inline code | ${groupedFailures.preCodeChip.length === 0 ? "passa" : "falha"} | ${groupedFailures.preCodeChip.length === 0 ? "estilos computados sem fundo, borda, padding ou raio próprios" : `${groupedFailures.preCodeChip.length} ocorrência(s) com estilo de chip`} |`,
    `| snippets técnicos têm highlight semântico | ${groupedFailures.highlight.length === 0 ? "passa" : "falha"} | ${groupedFailures.highlight.length === 0 ? "blocos técnicos usam classes de highlight ou são texto literal permitido" : `${groupedFailures.highlight.length} bloco(s) técnico(s) sem highlight`} |`,
    `| tabelas usam superfície estruturada | ${tableThemeFailure ? "falha" : "passa"} | ${tableThemeFailure ? "há célula de tabela fora do contrato escuro" : "td usa superfície escura e th usa variação escura"} |`,
    `| contraste mínimo em texto e código | ${groupedFailures.contrast.length === 0 ? "passa" : "falha"} | ${groupedFailures.contrast.length === 0 ? "amostras renderizadas com contraste >= 4.5:1" : `${groupedFailures.contrast.length} amostra(s) abaixo de 4.5:1`} |`,
    `| visuais conceituais não usam \`<pre>\` como atalho | ${groupedFailures.conceptualPre.length === 0 ? "passa" : "falha"} | ${groupedFailures.conceptualPre.length === 0 ? "nenhum <pre> suspeito sem exceção ASCII explícita" : `${groupedFailures.conceptualPre.length} bloco(s) visual(is) em <pre> sem exceção completa`} |`,
    `| página sem overflow horizontal global | ${groupedFailures.overflow.length === 0 ? "passa" : "falha"} | ${groupedFailures.overflow.length === 0 ? "desktop e mobile sem overflow global" : `${groupedFailures.overflow.length} viewport(s) com overflow global`} |`,
    `| assets externos inesperados | ${groupedFailures.externalRequests.length === 0 ? "passa" : "falha"} | ${groupedFailures.externalRequests.length === 0 ? "nenhuma requisição http(s) observada" : `${groupedFailures.externalRequests.length} requisição(ões) bloqueada(s)`} |`,
    "",
    "## Checks de largura de conteúdo",
    "",
    "| Check | Status | Evidência |",
    "|---|---|---|",
    `| parágrafos comuns ocupam a largura útil | ${paragraphFailure ? "falha" : "passa"} | ${widthEvidence} |`,
    `| callouts comuns ocupam a largura útil | ${calloutFailure ? "falha" : "passa"} | ${widthEvidence} |`,
    `| nenhuma coluna textual estreita sem motivo | ${groupedFailures.contentWidth.length === 0 ? "passa" : "falha"} | ${widthEvidence} |`,
    "",
    "## Inspeção visual do agente",
    "",
    "- Hierarquia visual: screenshots geradas; o agente deve confirmar antes da entrega.",
    "- Leitura mobile: screenshots geradas; o agente deve confirmar antes da entrega.",
    "- Problemas observados: registrar aqui qualquer falha vista nas screenshots.",
    "",
    "## Falhas",
    "",
    failureText.length ? failureText.join("\n") : "Nenhuma falha mecânica detectada pelo script.",
    "",
    "## Resultado da rodada",
    "",
    `- HTML precisa reescrita: ${status === "passa" ? "não" : "sim"}`,
    "- Se sim, corrigir `roadmap.html` ou CSS e reiniciar a rodada global.",
    "",
  ].join("\n");
  fs.writeFileSync(targets.visualAuditPath, audit, "utf-8");
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const targets = resolveTargets(args);
  fs.mkdirSync(targets.internalDir, { recursive: true });
  fs.mkdirSync(targets.visualPipeDir, { recursive: true });
  assertInside(targets.playwrightDir, targets.visualPipeDir, ".roadmap/pipeline/05-visual-render/playwright");
  fs.rmSync(targets.playwrightDir, { recursive: true, force: true });
  fs.mkdirSync(targets.playwrightDir, { recursive: true });

  const externalRequests = [];
  const browser = await chromium.launch({ headless: true });
  const renderResults = [];
  try {
    for (const viewport of VIEWPORTS) {
      renderResults.push(await renderViewport(browser, targets, viewport, externalRequests));
    }
  } finally {
    await browser.close();
  }

  const groupedFailures = {
    theme: darkThemeFailures(renderResults),
    preCodeChip: preCodeChipFailures(renderResults),
    highlight: highlightFailures(renderResults),
    overflow: overflowFailures(renderResults),
    contentWidth: contentWidthFailures(renderResults),
    contrast: contrastFailures(renderResults),
    externalRequests: externalRequestFailures(externalRequests),
    conceptualPre: conceptualPreFailures(renderResults),
  };

  const renderChecks = {
    status: Object.values(groupedFailures).flat().length === 0 ? "passa" : "falha",
    generatedAt: new Date().toISOString(),
    html: targets.htmlPath,
    viewports: renderResults,
    failures: groupedFailures,
  };
  fs.writeFileSync(targets.renderChecksPath, `${JSON.stringify(renderChecks, null, 2)}\n`, "utf-8");
  writeAudit(targets, renderResults, groupedFailures);

  const failures = Object.values(groupedFailures).flat();
  if (failures.length > 0) {
    console.error("falha: auditoria visual renderizada do roadmap inválida");
    for (const [group, items] of Object.entries(groupedFailures)) {
      if (items.length > 0) {
        console.error(`- ${group}: ${items.length}`);
      }
    }
    return 1;
  }

  console.log("passa: auditoria visual renderizada do roadmap válida");
  return 0;
}

run().then(
  (exitCode) => {
    process.exitCode = exitCode;
  },
  (error) => {
    console.error("falha: não foi possível executar auditoria visual renderizada do roadmap");
    console.error(error instanceof Error ? error.message : String(error));
    console.error(usage());
    process.exitCode = 1;
  },
);
