#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { pathToFileURL } from "node:url";

import { chromium } from "playwright";

const NODE_SLUG_RE = /^\d{2}-[a-z0-9][a-z0-9-]*$/;
const LEVELS = new Set(["basico", "intermediario", "avancado"]);
const VIEWPORTS = [
  { name: "desktop", width: 1280, height: 900, isMobile: false },
  { name: "mobile", width: 390, height: 844, isMobile: true },
];

function usage() {
  return [
    "Uso:",
    "  node <skill-dir>/node-pages/scripts/check_visual_render.mjs --roadmap-dir <roadmap-dir> --level <level> --node <node-slug>",
    "  node <skill-dir>/node-pages/scripts/check_visual_render.mjs --html <node-dir>/node.html",
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

  const hasHtml = Boolean(parsed.html);
  const hasRoadmapNode = Boolean(parsed["roadmap-dir"] && parsed.level && parsed.node);
  if (hasHtml === hasRoadmapNode) {
    throw new Error("informe --html ou --roadmap-dir com --level e --node");
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
  let roadmapDir;
  let level;
  let levelDir;
  let nodeSlug;
  let nodeDir;
  let htmlPath;

  if (args.html) {
    htmlPath = path.resolve(args.html);
    if (path.basename(htmlPath) !== "node.html") {
      throw new Error("--html deve apontar para um arquivo node.html");
    }
    nodeDir = path.dirname(htmlPath);
    nodeSlug = path.basename(nodeDir);
    levelDir = path.dirname(nodeDir);
    level = path.basename(levelDir);
    roadmapDir = path.dirname(levelDir);
  } else {
    roadmapDir = path.resolve(args["roadmap-dir"]);
    level = args.level;
    nodeSlug = args.node;
    if (nodeSlug.includes("..") || nodeSlug.includes("/") || nodeSlug.includes("\\")) {
      throw new Error("node slug contém caminho ou travessia");
    }
    levelDir = path.resolve(roadmapDir, level);
    nodeDir = path.resolve(levelDir, nodeSlug);
    htmlPath = path.resolve(nodeDir, "node.html");
  }

  if (!LEVELS.has(level)) {
    throw new Error("level deve ser basico, intermediario ou avancado");
  }
  if (!NODE_SLUG_RE.test(nodeSlug)) {
    throw new Error("node slug deve seguir o formato NN-slug");
  }
  if (!fs.existsSync(roadmapDir) || !fs.statSync(roadmapDir).isDirectory()) {
    throw new Error(`roadmap dir não existe: ${roadmapDir}`);
  }
  if (!fs.existsSync(htmlPath) || !fs.statSync(htmlPath).isFile()) {
    throw new Error(`node.html ausente: ${htmlPath}`);
  }

  assertInside(levelDir, roadmapDir, "level dir");
  assertInside(nodeDir, levelDir, "node dir");
  if (nodeDir === levelDir || nodeDir === roadmapDir) {
    throw new Error("node dir não pode ser a pasta do nível nem a pasta do roadmap");
  }

  const editorialDir = path.resolve(nodeDir, ".editorial");
  const visualPipeDir = path.resolve(editorialDir, "pipeline", "05-visual-render");
  const playwrightDir = path.resolve(visualPipeDir, "playwright");
  assertInside(editorialDir, nodeDir, ".editorial");
  assertInside(visualPipeDir, editorialDir, ".editorial/pipeline/05-visual-render");
  assertInside(playwrightDir, visualPipeDir, ".editorial/pipeline/05-visual-render/playwright");
  if (visualPipeDir === editorialDir) {
    throw new Error("pipe visual não pode ser a pasta .editorial inteira");
  }

  return {
    roadmapDir,
    level,
    levelDir,
    nodeSlug,
    nodeId: `${level}/${nodeSlug}`,
    nodeDir,
    htmlPath,
    editorialDir,
    visualPipeDir,
    playwrightDir,
    visualAuditPath: path.resolve(visualPipeDir, "visual-audit.md"),
    renderChecksPath: path.resolve(visualPipeDir, "render-checks.json"),
  };
}

function pxNumber(value) {
  const parsed = Number.parseFloat(String(value || "0"));
  return Number.isFinite(parsed) ? parsed : 0;
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

function inlineCodeFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    for (const inline of result.inlineCodeStyles) {
      const distinguishable =
        colorAlpha(inline.backgroundColor) > 0.01 ||
        hasPositiveBoxValue(inline.borderWidths) ||
        hasPositiveBoxValue(inline.paddings);
      if (!distinguishable) {
        failures.push({
          viewport: result.viewport.name,
          index: inline.index,
          text: inline.text,
        });
      }
    }
  }

  return failures;
}

function contrastFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    for (const sample of result.contrastSamples) {
      if (sample.ratio !== null && sample.ratio < 4.5) {
        failures.push({
          viewport: result.viewport.name,
          label: sample.label,
          text: sample.text,
          ratio: sample.ratio,
          color: sample.color,
          backgroundColor: sample.backgroundColor,
        });
      }
    }
  }

  return failures;
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
        failures.push({
          viewport: result.viewport.name,
          ...item,
        });
      }
    }
  }

  return failures;
}

function externalRequestFailures(externalRequests) {
  return [...new Set(externalRequests)].map((url) => ({ url }));
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
      if (parts.length < 3) {
        return null;
      }
      const rgb = parts.slice(0, 3).map((part) => Number.parseFloat(part));
      const alpha = parts.length >= 4 ? Number.parseFloat(parts[3]) : 1;
      if (rgb.some((valuePart) => !Number.isFinite(valuePart))) {
        return null;
      }
      return {
        r: rgb[0],
        g: rgb[1],
        b: rgb[2],
        a: Number.isFinite(alpha) ? alpha : 1,
      };
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
      const foregroundLuminance = luminance(foregroundColor);
      const backgroundLuminance = luminance(backgroundColor);
      const light = Math.max(foregroundLuminance, backgroundLuminance);
      const dark = Math.min(foregroundLuminance, backgroundLuminance);
      return Number(((light + 0.05) / (dark + 0.05)).toFixed(2));
    }

    function isVisible(element) {
      const style = window.getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return (
        style.display !== "none" &&
        style.visibility !== "hidden" &&
        rect.width > 0 &&
        rect.height > 0
      );
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

    function summarizeStyle(element, index) {
      const style = window.getComputedStyle(element);
      return {
        index,
        text: element.textContent.trim().slice(0, 120),
        color: style.color,
        backgroundColor: style.backgroundColor,
        effectiveBackgroundColor: effectiveBackground(element),
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

    function looksTechnical(text) {
      const trimmed = text.trim();
      return (
        /[=;{}[\]:]/.test(trimmed) ||
        /^\s*[\w.-]+\s+\S+/m.test(trimmed) ||
        /<[^>]+>/.test(trimmed)
      );
    }

    const preBlocks = Array.from(document.querySelectorAll("pre")).map((pre, index) => {
      const text = pre.textContent.trim();
      const asciiReason = pre.getAttribute("data-ascii-reason") || "";
      return {
        index,
        text: text.slice(0, 160),
        hasCode: Boolean(pre.querySelector("code")),
        hasHighlight: hasHighlightClass(pre),
        isConceptualVisual: isConceptualVisualPre(pre, text),
        hasAsciiException: pre.getAttribute("data-ascii-exception") === "true",
        asciiReason,
        looksTechnical: looksTechnical(text),
        className: pre.className,
        ariaLabel: pre.getAttribute("aria-label") || "",
      };
    });

    const preCodeStyles = Array.from(document.querySelectorAll("pre code")).map(
      (element, index) => summarizeStyle(element, index),
    );

    const inlineCodeStyles = Array.from(document.querySelectorAll("code"))
      .filter((element) => !element.closest("pre"))
      .map((element, index) => summarizeStyle(element, index));

    const sampleSelectors = [
      ["body", "body"],
      ["p", "parágrafo"],
      ["li", "item de lista"],
      ["td", "célula de tabela"],
      ["th", "cabeçalho de tabela"],
      ["a", "link"],
      ["code:not(pre code)", "inline code"],
      ["pre", "bloco de código"],
      ["pre code", "conteúdo de bloco de código"],
      [".syntax-key", "syntax-key"],
      [".syntax-op", "syntax-op"],
      [".syntax-value", "syntax-value"],
      [".syntax-comment", "syntax-comment"],
      [".syntax-risk", "syntax-risk"],
    ];

    const contrastSamples = [];
    for (const [selector, label] of sampleSelectors) {
      const elements = Array.from(document.querySelectorAll(selector))
        .filter(isVisible)
        .slice(0, 8);
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

    const documentElement = document.documentElement;
    const body = document.body;
    const clientWidth = documentElement.clientWidth;
    const scrollWidth = Math.max(
      documentElement.scrollWidth,
      body ? body.scrollWidth : 0,
    );
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
          ".card, table, pre, .tag, .small, .step, .risk-step, .position-strip, .contract-map, .visual-block, .content-grid, .timeline, .flow-steps, .state-grid, .topology, .lane-map, .lane",
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

    return {
      title: document.title,
      preBlocks,
      preCodeStyles,
      inlineCodeStyles,
      contrastSamples,
      contentWidths,
      overflow: {
        clientWidth,
        scrollWidth,
        hasGlobalOverflow: scrollWidth > clientWidth + 1,
      },
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

  return {
    viewport,
    screenshotPath,
    ...data,
  };
}

function failureSection(title, items, renderItem) {
  if (items.length === 0) {
    return "";
  }

  return [
    `### ${title}`,
    "",
    ...items.flatMap((item) => renderItem(item)),
    "",
  ].join("\n");
}

function writeAudit(targets, renderResults, groupedFailures) {
  const failures = [
    ...groupedFailures.preCodeChip,
    ...groupedFailures.highlight,
    ...groupedFailures.conceptualPre,
    ...groupedFailures.inlineCode,
    ...groupedFailures.contrast,
    ...groupedFailures.overflow,
    ...groupedFailures.contentWidth,
    ...groupedFailures.externalRequests,
  ];
  const status = failures.length === 0 ? "passa" : "falha";

  const screenshotRows = renderResults.map((result) => {
    const relative = path.relative(targets.nodeDir, result.screenshotPath);
    const note = result.overflow.hasGlobalOverflow
      ? `overflow global: ${result.overflow.scrollWidth}px para ${result.overflow.clientWidth}px`
      : "screenshot gerada";
    return `| ${result.viewport.name} | \`${relative}\` | ${note} |`;
  });

  const checkRows = [
    [
      "`pre code` não herda chip de inline code",
      groupedFailures.preCodeChip.length === 0 ? "passa" : "falha",
      groupedFailures.preCodeChip.length === 0
        ? "estilos computados sem fundo, borda, padding ou raio próprios"
        : `${groupedFailures.preCodeChip.length} ocorrência(s) com estilo de chip`,
    ],
    [
      "snippets técnicos têm highlight semântico",
      groupedFailures.highlight.length === 0 ? "passa" : "falha",
      groupedFailures.highlight.length === 0
        ? "blocos técnicos usam classes de highlight ou são texto literal permitido"
        : `${groupedFailures.highlight.length} bloco(s) técnico(s) sem highlight`,
    ],
    [
      "visuais conceituais não usam `<pre>` como atalho",
      groupedFailures.conceptualPre.length === 0 ? "passa" : "falha",
      groupedFailures.conceptualPre.length === 0
        ? "nenhum `<pre>` suspeito sem exceção ASCII explícita"
        : `${groupedFailures.conceptualPre.length} bloco(s) visual(is) em <pre> sem exceção completa`,
    ],
    [
      "contraste mínimo em texto e código",
      groupedFailures.contrast.length === 0 ? "passa" : "falha",
      groupedFailures.contrast.length === 0
        ? "amostras renderizadas com contraste >= 4.5:1"
        : `${groupedFailures.contrast.length} amostra(s) abaixo de 4.5:1`,
    ],
    [
      "página sem overflow horizontal global",
      groupedFailures.overflow.length === 0 ? "passa" : "falha",
      groupedFailures.overflow.length === 0
        ? "desktop e mobile sem overflow horizontal global"
        : `${groupedFailures.overflow.length} viewport(s) com overflow global`,
    ],
    [
      "texto comum ocupa largura útil",
      groupedFailures.contentWidth.length === 0 ? "passa" : "falha",
      groupedFailures.contentWidth.length === 0
        ? "parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop"
        : `${groupedFailures.contentWidth.length} bloco(s) textual(is) estreito(s)`,
    ],
    [
      "mobile legível sem sobreposição óbvia",
      groupedFailures.overflow.length === 0 ? "passa" : "falha",
      groupedFailures.overflow.length === 0
        ? "sem overflow global; agente ainda deve inspecionar screenshot mobile"
        : "overflow global exige revisão antes da inspeção final",
    ],
    [
      "assets externos inesperados",
      groupedFailures.externalRequests.length === 0 ? "passa" : "falha",
      groupedFailures.externalRequests.length === 0
        ? "nenhuma requisição http(s) observada"
        : `${groupedFailures.externalRequests.length} requisição(ões) bloqueada(s)`,
    ],
  ];

  const failureText = [
    failureSection("`pre code` com estilo de chip", groupedFailures.preCodeChip, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      `- Por que falha: ${item.reason}.`,
      `- Revisão obrigatória: defina \`pre code\` com fundo transparente, borda 0, padding 0 e \`font: inherit\`.`,
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Snippet técnico sem highlight", groupedFailures.highlight, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      "- Por que falha: snippet técnico precisa de destaque semântico mínimo.",
      "- Revisão obrigatória: adicionar spans/classes `syntax-*` ou justificar como texto literal excepcional.",
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Visual conceitual em `<pre>`", groupedFailures.conceptualPre, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, bloco ${item.index}.`,
      `- Por que falha: ${item.reason}.`,
      "- Revisão obrigatória: trocar por componente HTML/CSS ou declarar exceção ASCII com `data-ascii-exception=\"true\"` e `data-ascii-reason`.",
      `- Classe: \`${item.className || "(sem classe)"}\``,
      `- Aria-label: \`${item.ariaLabel || "(sem aria-label)"}\``,
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Inline code sem distinção visual", groupedFailures.inlineCode, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, inline code ${item.index}.`,
      "- Por que falha: inline `code` ficou indistinguível do texto ao redor.",
      "- Revisão obrigatória: restaurar fundo, borda ou padding legível para inline `code`.",
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Contraste insuficiente", groupedFailures.contrast, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, ${item.label}.`,
      `- Por que falha: contraste ${item.ratio}:1 entre ${item.color} e ${item.backgroundColor}.`,
      "- Revisão obrigatória: ajustar cor de texto, fundo ou token.",
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Overflow horizontal global", groupedFailures.overflow, (item) => [
      `- Onde apareceu: viewport ${item.viewport}.`,
      `- Por que falha: scrollWidth ${item.scrollWidth}px excede clientWidth ${item.clientWidth}px.`,
      "- Revisão obrigatória: corrigir largura, tabela, card, visual ou bloco de código que vaza do viewport.",
      "",
    ]),
    failureSection("Bloco textual estreito", groupedFailures.contentWidth, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, seletor ${item.selector}, bloco ${item.index}.`,
      `- Por que falha: largura ${item.width}px para main ${item.mainWidth}px (${item.ratio}).`,
      "- Revisão obrigatória: remover max-width local ou reduzir a largura estrutural de `main`.",
      `- Trecho: \`${item.text}\``,
      "",
    ]),
    failureSection("Asset externo bloqueado", groupedFailures.externalRequests, (item) => [
      `- Onde apareceu: ${item.url}.`,
      "- Por que falha: o HTML do node deve ser autocontido para esta auditoria.",
      "- Revisão obrigatória: remover dependência remota ou incorporar alternativa local/autocontida.",
      "",
    ]),
  ].filter(Boolean).join("\n");

  const renderChecksRelative = path.relative(targets.nodeDir, targets.renderChecksPath);
  const audit = [
    "# Visual render audit",
    "",
    "## Metadados",
    "",
    `- Roadmap: ${path.basename(targets.roadmapDir)}`,
    `- Level: ${targets.level}`,
    `- Node: ${targets.nodeSlug}`,
    `- Node ID: ${targets.nodeId}`,
    "- Rodada: gerada pelo script Playwright",
    `- Data: ${new Date().toISOString()}`,
    `- HTML auditado: \`${path.relative(targets.nodeDir, targets.htmlPath)}\``,
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
    ...checkRows.map((row) => `| ${row[0]} | ${row[1]} | ${row[2]} |`),
    "",
    "## Checks de largura de conteúdo",
    "",
    "| Check | Status | Evidência |",
    "|---|---|---|",
    `| parágrafos comuns ocupam a largura útil | ${groupedFailures.contentWidth.some((item) => ["p", "ul", "ol", ".lead"].includes(item.selector)) ? "falha" : "passa"} | ${groupedFailures.contentWidth.length === 0 ? ">= 90% da largura útil no desktop" : `${groupedFailures.contentWidth.length} bloco(s) estreito(s)`} |`,
    `| callouts comuns ocupam a largura útil | ${groupedFailures.contentWidth.some((item) => item.selector === ".callout") ? "falha" : "passa"} | ${groupedFailures.contentWidth.length === 0 ? ">= 90% da largura útil no desktop" : `${groupedFailures.contentWidth.length} bloco(s) estreito(s)`} |`,
    `| nenhuma coluna textual estreita sem motivo | ${groupedFailures.contentWidth.length === 0 ? "passa" : "falha"} | ${groupedFailures.contentWidth.length === 0 ? "nenhum bloco textual comum abaixo do limite" : "há bloco textual comum abaixo do limite"} |`,
    "",
    "## Inspeção visual do agente",
    "",
    "- Cores dos exemplos: screenshots geradas; o agente deve confirmar antes da entrega.",
    "- Leitura dos snippets: screenshots geradas; o agente deve confirmar antes da entrega.",
    "- Hierarquia visual: screenshots geradas; o agente deve confirmar antes da entrega.",
    "- Problemas observados: registrar aqui qualquer falha vista nas screenshots.",
    "",
    "## Falhas",
    "",
    failureText || "Nenhuma falha mecânica detectada pelo script.",
    "",
    "## Resultado da rodada",
    "",
    `- HTML precisa reescrita: ${status === "passa" ? "não" : "sim"}`,
    "- Se sim, atualizar `.editorial/pipeline/05-visual-render/revision-plan.md` e reiniciar a rodada global depois da reescrita.",
    "",
  ].join("\n");

  fs.writeFileSync(targets.visualAuditPath, audit, "utf-8");
}

async function run() {
  const args = parseArgs(process.argv.slice(2));
  const targets = resolveTargets(args);

  fs.mkdirSync(targets.editorialDir, { recursive: true });
  fs.mkdirSync(targets.visualPipeDir, { recursive: true });
  assertInside(targets.playwrightDir, targets.visualPipeDir, ".editorial/pipeline/05-visual-render/playwright");
  fs.rmSync(targets.playwrightDir, { recursive: true, force: true });
  fs.mkdirSync(targets.playwrightDir, { recursive: true });

  const externalRequests = [];
  const browser = await chromium.launch({ headless: true });
  let renderResults = [];

  try {
    for (const viewport of VIEWPORTS) {
      renderResults.push(
        await renderViewport(browser, targets, viewport, externalRequests),
      );
    }
  } finally {
    await browser.close();
  }

  const groupedFailures = {
    preCodeChip: preCodeChipFailures(renderResults),
    highlight: highlightFailures(renderResults),
    conceptualPre: conceptualPreFailures(renderResults),
    inlineCode: inlineCodeFailures(renderResults),
    contrast: contrastFailures(renderResults),
    overflow: overflowFailures(renderResults),
    contentWidth: contentWidthFailures(renderResults),
    externalRequests: externalRequestFailures(externalRequests),
  };

  const renderChecks = {
    status:
      Object.values(groupedFailures).flat().length === 0 ? "passa" : "falha",
    generatedAt: new Date().toISOString(),
    html: targets.htmlPath,
    viewports: renderResults,
    failures: groupedFailures,
  };
  fs.writeFileSync(
    targets.renderChecksPath,
    `${JSON.stringify(renderChecks, null, 2)}\n`,
    "utf-8",
  );

  writeAudit(targets, renderResults, groupedFailures);

  const failures = Object.values(groupedFailures).flat();
  if (failures.length > 0) {
    console.error("falha: auditoria visual renderizada inválida");
    for (const [group, items] of Object.entries(groupedFailures)) {
      if (items.length > 0) {
        console.error(`- ${group}: ${items.length}`);
      }
    }
    return 1;
  }

  console.log("passa: auditoria visual renderizada válida");
  return 0;
}

run().then(
  (exitCode) => {
    process.exitCode = exitCode;
  },
  (error) => {
    console.error("falha: não foi possível executar auditoria visual renderizada");
    console.error(error instanceof Error ? error.message : String(error));
    console.error(usage());
    process.exitCode = 1;
  },
);
