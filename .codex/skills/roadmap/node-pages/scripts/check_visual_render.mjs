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
const CANONICAL = {
  accentColor: "rgb(106, 174, 214)",
  nodeContextBackground: "rgb(36, 36, 36)",
  nodeFooterBackground: "rgba(0, 0, 0, 0)",
  nodeFooterLinkWeight: "400",
  nodeContextLinkWeight: "400",
};
const PLACEHOLDER_PATTERNS = [
  /\.\.\./,
  /agent must inspect/i,
  /register problems here/i,
  /registrar aqui/i,
  /agente deve confirmar/i,
  /deve confirmar antes da entrega/i,
  /problemas observados:\s*$/im,
  /problemas observados:\s*registrar/i,
];

function usage() {
  return [
    "Uso:",
    "  docker/runtime/run node <skill-dir>/node-pages/scripts/check_visual_render.mjs --self-test",
    "  docker/runtime/run node <skill-dir>/node-pages/scripts/check_visual_render.mjs --roadmap-dir <roadmap-dir> --level <level> --node <node-slug>",
    "  docker/runtime/run node <skill-dir>/node-pages/scripts/check_visual_render.mjs --html <node-dir>/node.html",
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

function closePx(actual, expected, tolerance = 0.25) {
  return Math.abs(pxNumber(actual) - expected) <= tolerance;
}

function allClosePx(values, expectedValues) {
  return values.length === expectedValues.length &&
    values.every((value, index) => closePx(value, expectedValues[index]));
}

function normalizedColor(value) {
  return String(value || "").replace(/\s+/g, " ").trim().toLowerCase();
}

function sameColor(actual, expected) {
  return normalizedColor(actual) === normalizedColor(expected);
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
  return {
    r: rgb[0],
    g: rgb[1],
    b: rgb[2],
    a: Number.isFinite(alpha) ? alpha : 1,
  };
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

function fixedComponentFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    const styles = result.componentStyles || {};
    const contexts = styles.nodeContext || [];
    if (contexts.length !== 1) {
      failures.push({
        viewport: result.viewport.name,
        component: ".node-context",
        property: "count",
        expected: "1",
        actual: String(contexts.length),
      });
    }
    for (const context of contexts) {
      const checks = [
        ["display", context.display, "grid", context.display === "grid"],
        ["gap", context.gap, "6px", closePx(context.gap, 6)],
        ["padding", context.paddings.join(" "), "12px 14px 12px 14px", allClosePx(context.paddings, [12, 14, 12, 14])],
        ["margin", context.margins.join(" "), "0px 0px 18px 0px", allClosePx(context.margins, [0, 0, 18, 0])],
        ["border-width", context.borderWidths.join(" "), "1px 1px 1px 4px", allClosePx(context.borderWidths, [1, 1, 1, 4])],
        ["border-radius", context.borderRadii.join(" "), "6px", allClosePx(context.borderRadii, [6, 6, 6, 6])],
        ["background", context.backgroundColor, CANONICAL.nodeContextBackground, sameColor(context.backgroundColor, CANONICAL.nodeContextBackground)],
      ];
      for (const [property, actual, expected, ok] of checks) {
        if (!ok) {
          failures.push({
            viewport: result.viewport.name,
            component: ".node-context",
            property,
            expected,
            actual,
          });
        }
      }
    }

    for (const link of styles.nodeContextLinks || []) {
      const checks = [
        ["color", link.color, CANONICAL.accentColor, sameColor(link.color, CANONICAL.accentColor)],
        ["font-weight", link.fontWeight, CANONICAL.nodeContextLinkWeight, link.fontWeight === CANONICAL.nodeContextLinkWeight],
        ["text-decoration-line", link.textDecorationLine, "underline", /\bunderline\b/.test(link.textDecorationLine || "")],
      ];
      for (const [property, actual, expected, ok] of checks) {
        if (!ok) {
          failures.push({
            viewport: result.viewport.name,
            component: ".node-context a",
            property,
            expected,
            actual,
          });
        }
      }
    }

    const footers = styles.nodeFooter || [];
    if (footers.length !== 1) {
      failures.push({
        viewport: result.viewport.name,
        component: "footer.node-footer",
        property: "count",
        expected: "1",
        actual: String(footers.length),
      });
    }
    for (const footer of footers) {
      const checks = [
        ["border-top-width", footer.borderWidths[0], "0px", closePx(footer.borderWidths[0], 0)],
        ["padding", footer.paddings.join(" "), "0px", allClosePx(footer.paddings, [0, 0, 0, 0])],
        ["background", footer.backgroundColor, CANONICAL.nodeFooterBackground, sameColor(footer.backgroundColor, CANONICAL.nodeFooterBackground)],
      ];
      for (const [property, actual, expected, ok] of checks) {
        if (!ok) {
          failures.push({
            viewport: result.viewport.name,
            component: "footer.node-footer",
            property,
            expected,
            actual,
          });
        }
      }
    }

    for (const link of styles.nodeFooterLinks || []) {
      const checks = [
        ["color", link.color, CANONICAL.accentColor, sameColor(link.color, CANONICAL.accentColor)],
        ["font-weight", link.fontWeight, CANONICAL.nodeFooterLinkWeight, link.fontWeight === CANONICAL.nodeFooterLinkWeight],
        ["text-decoration-line", link.textDecorationLine, "underline", /\bunderline\b/.test(link.textDecorationLine || "")],
      ];
      for (const [property, actual, expected, ok] of checks) {
        if (!ok) {
          failures.push({
            viewport: result.viewport.name,
            component: ".node-footer a",
            property,
            expected,
            actual,
          });
        }
      }
    }
  }

  return failures;
}

function terminalDividerFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    const candidates = result.componentStyles?.terminalDividerCandidates || [];
    for (const candidate of candidates) {
      if (pxNumber(candidate.borderWidths[0]) > 0.1) {
        failures.push({
          viewport: result.viewport.name,
          index: candidate.index,
          text: candidate.text,
          borderTopWidth: candidate.borderWidths[0],
          borderTopStyle: candidate.borderStyles[0],
        });
      }
    }
  }

  return failures;
}

function visualPrimitiveFailures(renderResults) {
  const failures = [];

  for (const result of renderResults) {
    const primitives = result.visualPrimitives || {};
    for (const tag of primitives.tags || []) {
      const displayOk = tag.display === "inline-flex" || tag.display === "flex";
      const shortTag = String(tag.text || "").length <= 40;
      const stretched =
        shortTag &&
        tag.parentWidthPx > 120 &&
        tag.widthPx > tag.parentWidthPx * 0.85;
      const checks = [
        ["display", tag.display, "inline-flex ou flex", displayOk],
        ["justify-self", tag.justifySelf, "start", tag.justifySelf === "start"],
        ["align-self", tag.alignSelf, "start", tag.alignSelf === "start"],
        [
          "width",
          `${tag.widthPx}px de ${tag.parentWidthPx}px`,
          "largura intrínseca, sem ocupar quase todo o pai",
          !stretched,
        ],
      ];
      for (const [property, actual, expected, ok] of checks) {
        if (!ok) {
          failures.push({
            viewport: result.viewport.name,
            primitive: ".tag",
            property,
            expected,
            actual,
            text: tag.text,
          });
        }
      }
    }

    for (const step of primitives.flowStepAfter || []) {
      const contentActive = step.content && step.content !== "none" && step.content !== "normal";
      const displayActive = step.display && step.display !== "none";
      const hasBox =
        pxNumber(step.width) > 0.1 ||
        pxNumber(step.height) > 0.1 ||
        hasPositiveBoxValue(step.borderWidths) ||
        colorAlpha(step.backgroundColor) > 0.01;
      if (contentActive && displayActive && hasBox) {
        failures.push({
          viewport: result.viewport.name,
          primitive: ".flow-steps > .flow-step::after",
          property: "pseudo-element",
          expected: "content none/display none/sem caixa",
          actual: `content ${step.content}, display ${step.display}, width ${step.width}, height ${step.height}`,
          text: step.text,
        });
      }
    }
  }

  return failures;
}

function auditPlaceholderFailures(auditText) {
  if (!/status geral:\s*passa/i.test(auditText)) {
    return [];
  }
  return PLACEHOLDER_PATTERNS
    .filter((pattern) => pattern.test(auditText))
    .map((pattern) => ({ pattern: String(pattern) }));
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

    function isDarkSurface(background) {
      const parsed = parseColor(background);
      return Boolean(parsed && parsed.a > 0.01 && luminance(parsed) <= 0.18);
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
      const rect = element.getBoundingClientRect();
      const parentRect = element.parentElement
        ? element.parentElement.getBoundingClientRect()
        : null;
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
        borderStyles: [
          style.borderTopStyle,
          style.borderRightStyle,
          style.borderBottomStyle,
          style.borderLeftStyle,
        ],
        paddings: [
          style.paddingTop,
          style.paddingRight,
          style.paddingBottom,
          style.paddingLeft,
        ],
        margins: [
          style.marginTop,
          style.marginRight,
          style.marginBottom,
          style.marginLeft,
        ],
        borderRadii: [
          style.borderTopLeftRadius,
          style.borderTopRightRadius,
          style.borderBottomRightRadius,
          style.borderBottomLeftRadius,
        ],
        display: style.display,
        gap: style.gap,
        fontWeight: style.fontWeight,
        textDecorationLine: style.textDecorationLine,
        fontFamily: style.fontFamily,
        fontSize: style.fontSize,
        width: style.width,
        maxWidth: style.maxWidth,
        justifySelf: style.justifySelf,
        alignSelf: style.alignSelf,
        widthPx: Number(rect.width.toFixed(2)),
        heightPx: Number(rect.height.toFixed(2)),
        parentWidthPx: parentRect ? Number(parentRect.width.toFixed(2)) : 0,
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
      [".tag", "tag"],
      [".small", "texto auxiliar"],
      [".route-label", "route-label"],
      [".node-context", "contexto de node"],
      [".node-context a", "link do contexto de node"],
      [".node-footer", "rodapé de referências"],
      [".node-footer a", "link do rodapé de referências"],
      [
        ".flow-step, .step, .state-card, .stream-card, .event-card, .group-card, .tool-card, .part, .handoff-card, .lane, .boundary-card",
        "visual customizado",
      ],
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
    const themeSurfaceSelectors = [
      ["body", "body"],
      ["main", "main"],
      [".node-context", ".node-context"],
      [".node-footer", ".node-footer"],
      [".reference-item", ".reference-item"],
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
          ".card, table, pre, .tag, .small, .step, .risk-step, .position-strip, .contract-map, .visual-block, .content-grid, .timeline, .timeline-step, .flow-steps, .flow-step, .state-grid, .state-card, .topology, .topology-node, .lane-map, .lane, .stream-card, .event-card, .group-card, .tool-card, .part, .group-shell, .umbrella-map, .process-card, .visual-card, .concept-card, .path-card, .decision-card, .stage, .segment, .panel, .box, .map-card, .layer, .node-card, .mini-card, .boundary-card, .handoff-card, .flow-mini",
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

    const componentStyles = {
      nodeContext: Array.from(document.querySelectorAll(".node-context"))
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
      nodeContextLinks: Array.from(document.querySelectorAll(".node-context a"))
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
      nodeFooter: Array.from(document.querySelectorAll("footer.node-footer"))
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
      nodeFooterLinks: Array.from(document.querySelectorAll(".node-footer a"))
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
      terminalDividerCandidates: Array.from(
        document.querySelectorAll(".refs, .references, .final-note, .node-footer, .node-closing"),
      )
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
    };

    const visualPrimitives = {
      tags: Array.from(document.querySelectorAll(".tag"))
        .filter(isVisible)
        .map((element, index) => summarizeStyle(element, index)),
      flowStepAfter: Array.from(document.querySelectorAll(".flow-steps > .flow-step"))
        .filter(isVisible)
        .map((element, index) => {
          const pseudo = window.getComputedStyle(element, "::after");
          return {
            index,
            text: element.textContent.trim().slice(0, 120),
            content: pseudo.content,
            display: pseudo.display,
            width: pseudo.width,
            height: pseudo.height,
            borderWidths: [
              pseudo.borderTopWidth,
              pseudo.borderRightWidth,
              pseudo.borderBottomWidth,
              pseudo.borderLeftWidth,
            ],
            backgroundColor: pseudo.backgroundColor,
          };
        }),
    };

    return {
      title: document.title,
      theme: {
        marker: documentElement.getAttribute("data-visual-theme") || "",
        colorScheme: window.getComputedStyle(documentElement).colorScheme || window.getComputedStyle(body).colorScheme || "",
        surfaceSamples: themeSurfaceSamples,
      },
      preBlocks,
      preCodeStyles,
      inlineCodeStyles,
      componentStyles,
      visualPrimitives,
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
    ...groupedFailures.theme,
    ...groupedFailures.fixedComponent,
    ...groupedFailures.terminalDivider,
    ...groupedFailures.visualPrimitive,
    ...groupedFailures.preCodeChip,
    ...groupedFailures.highlight,
    ...groupedFailures.conceptualPre,
    ...groupedFailures.inlineCode,
    ...groupedFailures.contrast,
    ...groupedFailures.overflow,
    ...groupedFailures.contentWidth,
    ...groupedFailures.externalRequests,
    ...groupedFailures.auditPlaceholder,
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
      "tema visual `notion-dark` aplicado",
      groupedFailures.theme.length === 0 ? "passa" : "falha",
      groupedFailures.theme.length === 0
        ? "marcador, color-scheme e superfícies escuras confirmados"
        : `${groupedFailures.theme.length} problema(s) de tema`,
    ],
    [
      "raiz CSS escura única, sem legado claro",
      groupedFailures.theme.length === 0 ? "passa" : "falha",
      groupedFailures.theme.length === 0
        ? "marcador, color-scheme e superfícies escuras confirmados"
        : `${groupedFailures.theme.length} problema(s) de tema`,
    ],
    [
      "`.node-context` usa estilo fixo",
      groupedFailures.fixedComponent.filter((item) => item.component === ".node-context").length === 0 ? "passa" : "falha",
      groupedFailures.fixedComponent.filter((item) => item.component === ".node-context").length === 0
        ? "estilos computados do contexto batem com o contrato"
        : `${groupedFailures.fixedComponent.filter((item) => item.component === ".node-context").length} divergência(s) no contexto`,
    ],
    [
      "`.node-context a` usa estilo fixo",
      groupedFailures.fixedComponent.filter((item) => item.component === ".node-context a").length === 0 ? "passa" : "falha",
      groupedFailures.fixedComponent.filter((item) => item.component === ".node-context a").length === 0
        ? "links do contexto usam cor, peso e sublinhado fixos"
        : `${groupedFailures.fixedComponent.filter((item) => item.component === ".node-context a").length} divergência(s) em links do contexto`,
    ],
    [
      "`footer.node-footer` usa forma e estilo fixos",
      groupedFailures.fixedComponent.filter((item) => item.component === "footer.node-footer" || item.component === ".node-footer a").length === 0 ? "passa" : "falha",
      groupedFailures.fixedComponent.filter((item) => item.component === "footer.node-footer" || item.component === ".node-footer a").length === 0
        ? "rodapé e links do rodapé batem com o contrato"
        : `${groupedFailures.fixedComponent.filter((item) => item.component === "footer.node-footer" || item.component === ".node-footer a").length} divergência(s) no rodapé`,
    ],
    [
      "divisores terminais não duplicam o divisor canônico",
      groupedFailures.terminalDivider.length === 0 ? "passa" : "falha",
      groupedFailures.terminalDivider.length === 0
        ? "containers terminais não possuem border-top próprio"
        : `${groupedFailures.terminalDivider.length} container(es) terminal(is) com border-top próprio`,
    ],
    [
      "primitivas visuais fixas não derivam estilo próprio",
      groupedFailures.visualPrimitive.length === 0 ? "passa" : "falha",
      groupedFailures.visualPrimitive.length === 0
        ? "tags renderizam compactas e flow-step não desenha conector duplicado"
        : `${groupedFailures.visualPrimitive.length} divergência(s) em tag ou flow-step`,
    ],
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
    [
      "auditoria sem placeholder manual",
      groupedFailures.auditPlaceholder.length === 0 ? "passa" : "falha",
      groupedFailures.auditPlaceholder.length === 0
        ? "campos de inspeção foram preenchidos com evidência concreta"
        : `${groupedFailures.auditPlaceholder.length} placeholder(s) encontrado(s)`,
    ],
  ];

  const failureText = [
    failureSection("Tema visual `notion-dark` inválido", groupedFailures.theme, (item) => [
      `- Onde apareceu: viewport ${item.viewport}${item.selector ? `, seletor ${item.selector}` : ""}.`,
      item.check === "dark-surface"
        ? `- Por que falha: superfície ${item.backgroundColor} não é escura o suficiente.`
        : `- Por que falha: ${item.check} atual \`${item.actual}\`; esperado \`${item.expected}\`.`,
      "- Revisão obrigatória: aplicar `data-visual-theme=\"notion-dark\"`, `color-scheme: dark` e os tokens escuros do sistema visual.",
      item.text ? `- Trecho: \`${item.text}\`` : "",
      "",
    ]),
    failureSection("Componente fixo com estilo divergente", groupedFailures.fixedComponent, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, componente ${item.component}.`,
      `- Por que falha: propriedade ${item.property} está \`${item.actual}\`; esperado \`${item.expected}\`.`,
      "- Revisão obrigatória: restaurar o CSS canônico do componente fixo no template.",
      "",
    ]),
    failureSection("Divisor terminal duplicado", groupedFailures.terminalDivider, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, candidato terminal ${item.index}.`,
      `- Por que falha: border-top ${item.borderTopWidth} ${item.borderTopStyle}.`,
      "- Revisão obrigatória: remover border-top do container terminal e deixar apenas a política canônica de headings.",
      item.text ? `- Trecho: \`${item.text}\`` : "",
      "",
    ]),
    failureSection("Primitiva visual fixa divergente", groupedFailures.visualPrimitive, (item) => [
      `- Onde apareceu: viewport ${item.viewport}, primitiva ${item.primitive}.`,
      `- Por que falha: propriedade ${item.property} está \`${item.actual}\`; esperado \`${item.expected}\`.`,
      "- Revisão obrigatória: restaurar a regra canônica no template e remover variação local no HTML gerado.",
      item.text ? `- Trecho: \`${item.text}\`` : "",
      "",
    ]),
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
    failureSection("Placeholder em auditoria visual", groupedFailures.auditPlaceholder, (item) => [
      `- Onde apareceu: padrão ${item.pattern}.`,
      "- Por que falha: auditoria marcada como passa não pode manter campo genérico sem inspeção.",
      "- Revisão obrigatória: preencher a inspeção com evidência concreta de desktop e mobile.",
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
    "- `.node-context`: estilo computado validado nos viewports desktop e mobile; screenshots salvas em `playwright/`.",
    "- `footer.node-footer`: estilo computado validado nos viewports desktop e mobile; screenshots salvas em `playwright/`.",
    "- Divisores: containers terminais sem `border-top` próprio quando os checks passam.",
    "- Tema escuro: marcador `notion-dark`, `color-scheme` e superfícies escuras registrados em `render-checks.json`.",
    "- Cores dos exemplos: contraste e superfícies amostrados pelo script; revisar falhas listadas abaixo se existirem.",
    "- Leitura dos snippets: chips inline, blocos `pre code` e highlight semântico medidos pelo script.",
    "- Hierarquia visual: screenshots desktop e mobile geradas para revisão visual da rodada.",
    "- Problemas observados: nenhuma falha mecânica quando o status geral é `passa`; falhas específicas aparecem na seção Falhas.",
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
  return audit;
}

function canonicalStyle(overrides = {}) {
  return {
    index: 0,
    text: "fixture",
    color: CANONICAL.accentColor,
    backgroundColor: "rgba(0, 0, 0, 0)",
    effectiveBackgroundColor: "rgb(25, 25, 25)",
    borderWidths: ["0px", "0px", "0px", "0px"],
    borderStyles: ["none", "none", "none", "none"],
    paddings: ["0px", "0px", "0px", "0px"],
    margins: ["0px", "0px", "0px", "0px"],
    borderRadii: ["0px", "0px", "0px", "0px"],
    display: "block",
    gap: "normal",
    fontWeight: "400",
    textDecorationLine: "underline",
    fontFamily: "Arial",
    fontSize: "18px",
    width: "auto",
    maxWidth: "100%",
    justifySelf: "start",
    alignSelf: "start",
    widthPx: 42,
    heightPx: 24,
    parentWidthPx: 240,
    ...overrides,
  };
}

function selfTestRenderResult() {
  return {
    viewport: { name: "desktop", width: 1280, height: 900, isMobile: false },
    componentStyles: {
      nodeContext: [
        canonicalStyle({
          backgroundColor: CANONICAL.nodeContextBackground,
          borderWidths: ["1px", "1px", "1px", "4px"],
          borderStyles: ["solid", "solid", "solid", "solid"],
          paddings: ["12px", "14px", "12px", "14px"],
          margins: ["0px", "0px", "18px", "0px"],
          borderRadii: ["6px", "6px", "6px", "6px"],
          display: "grid",
          gap: "6px",
        }),
      ],
      nodeContextLinks: [canonicalStyle()],
      nodeFooter: [
        canonicalStyle({
          backgroundColor: CANONICAL.nodeFooterBackground,
          textDecorationLine: "none",
        }),
      ],
      nodeFooterLinks: [canonicalStyle()],
      terminalDividerCandidates: [
        canonicalStyle({
          borderWidths: ["0px", "0px", "0px", "0px"],
          borderStyles: ["none", "none", "none", "none"],
        }),
      ],
    },
    visualPrimitives: {
      tags: [
        canonicalStyle({
          display: "inline-flex",
          justifySelf: "start",
          alignSelf: "start",
        }),
      ],
      flowStepAfter: [
        {
          index: 0,
          text: "fixture",
          content: "none",
          display: "none",
          width: "0px",
          height: "0px",
          borderWidths: ["0px", "0px", "0px", "0px"],
          backgroundColor: "rgba(0, 0, 0, 0)",
        },
      ],
    },
  };
}

function runSelfTest() {
  const failures = [];
  const canonical = selfTestRenderResult();
  if (fixedComponentFailures([canonical]).length !== 0) {
    failures.push("canonical fixed component styles should pass");
  }
  if (terminalDividerFailures([canonical]).length !== 0) {
    failures.push("canonical terminal divider styles should pass");
  }
  if (visualPrimitiveFailures([canonical]).length !== 0) {
    failures.push("canonical visual primitive styles should pass");
  }

  const brokenLink = JSON.parse(JSON.stringify(canonical));
  brokenLink.componentStyles.nodeContextLinks[0].fontWeight = "700";
  if (!fixedComponentFailures([brokenLink]).some((failure) => failure.component === ".node-context a")) {
    failures.push("node-context link weight drift should fail");
  }

  const brokenDivider = JSON.parse(JSON.stringify(canonical));
  brokenDivider.componentStyles.terminalDividerCandidates[0].borderWidths[0] = "1px";
  brokenDivider.componentStyles.terminalDividerCandidates[0].borderStyles[0] = "solid";
  if (terminalDividerFailures([brokenDivider]).length === 0) {
    failures.push("terminal border-top drift should fail");
  }

  const brokenTag = JSON.parse(JSON.stringify(canonical));
  brokenTag.visualPrimitives.tags[0].display = "block";
  if (!visualPrimitiveFailures([brokenTag]).some((failure) => failure.primitive === ".tag")) {
    failures.push("tag display drift should fail");
  }

  const stretchedTag = JSON.parse(JSON.stringify(canonical));
  stretchedTag.visualPrimitives.tags[0].widthPx = 238;
  stretchedTag.visualPrimitives.tags[0].parentWidthPx = 240;
  if (!visualPrimitiveFailures([stretchedTag]).some((failure) => failure.property === "width")) {
    failures.push("tag stretched width should fail");
  }

  const brokenFlowStep = JSON.parse(JSON.stringify(canonical));
  brokenFlowStep.visualPrimitives.flowStepAfter[0] = {
    ...brokenFlowStep.visualPrimitives.flowStepAfter[0],
    content: "\"\"",
    display: "block",
    width: "24px",
    height: "1px",
    backgroundColor: "rgb(51, 51, 51)",
  };
  if (!visualPrimitiveFailures([brokenFlowStep]).some((failure) => failure.primitive === ".flow-steps > .flow-step::after")) {
    failures.push("flow-step pseudo connector drift should fail");
  }

  const placeholderAudit = "## Status geral\n\nStatus geral: passa\n\n- Problemas observados: registrar aqui";
  if (auditPlaceholderFailures(placeholderAudit).length === 0) {
    failures.push("passing audit with placeholder should fail");
  }
  const concreteAudit = "## Status geral\n\nStatus geral: passa\n\n- Problemas observados: nenhuma falha mecânica detectada";
  if (auditPlaceholderFailures(concreteAudit).length !== 0) {
    failures.push("concrete passing audit should pass placeholder check");
  }

  if (failures.length > 0) {
    console.error("falha: self-test do visual checker falhou");
    for (const failure of failures) {
      console.error(`- ${failure}`);
    }
    return 1;
  }
  console.log("passa: self-test do visual checker cobre componentes fixos, divisores e placeholders");
  return 0;
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
    theme: darkThemeFailures(renderResults),
    fixedComponent: fixedComponentFailures(renderResults),
    terminalDivider: terminalDividerFailures(renderResults),
    visualPrimitive: visualPrimitiveFailures(renderResults),
    preCodeChip: preCodeChipFailures(renderResults),
    highlight: highlightFailures(renderResults),
    conceptualPre: conceptualPreFailures(renderResults),
    inlineCode: inlineCodeFailures(renderResults),
    contrast: contrastFailures(renderResults),
    overflow: overflowFailures(renderResults),
    contentWidth: contentWidthFailures(renderResults),
    externalRequests: externalRequestFailures(externalRequests),
    auditPlaceholder: [],
  };

  let auditText = writeAudit(targets, renderResults, groupedFailures);
  const placeholderFailures = auditPlaceholderFailures(auditText);
  if (placeholderFailures.length > 0) {
    groupedFailures.auditPlaceholder = placeholderFailures;
    auditText = writeAudit(targets, renderResults, groupedFailures);
  }

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

if (process.argv.slice(2).includes("--self-test")) {
  process.exitCode = runSelfTest();
} else {
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
}
