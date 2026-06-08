#!/usr/bin/env python3
"""Smoke tests for hardened node HTML shape validation."""

from __future__ import annotations

from check_html_shape import collect_failures


BASE_HTML = """<!doctype html>
<html lang="pt-BR" data-visual-theme="notion-dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Node canônico</title>
  <style>
    :root {
      color-scheme: dark;
      --page: #191919;
      --surface: #202020;
      --soft: #242424;
      --text: #e6e6e6;
      --heading: #f2f2f2;
      --muted: #a3a3a3;
      --border: #333333;
      --accent: #6aaed6;
    }
    body { margin: 0; color: var(--text); background: var(--page); }
    main { max-width: 1260px; margin: 0 auto; padding: 32px 28px 56px; }
    h2 { border-top: 1px solid var(--border); padding-top: 28px; margin-top: 32px; }
    .backlink { display: inline-flex; margin-bottom: 18px; font-weight: 700; }
    .lead { color: var(--muted); font-size: 19px; }
    .node-context { display: grid; gap: 6px; padding: 12px 14px; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 6px; background: var(--soft); margin: 0 0 18px; width: 100%; }
    .node-context p { margin: 0; }
    .node-context a { color: var(--accent); font-weight: 400; text-decoration-line: underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }
    .node-footer { margin: 0; padding: 0; border: 0; background: transparent; }
    .reference-list { display: grid; gap: 8px; margin: 8px 0 0; padding: 0; list-style: none; }
    .reference-item { display: grid; grid-template-columns: minmax(180px, 0.42fr) minmax(0, 1fr); gap: 10px; padding: 10px 12px; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); }
  </style>
</head>
<body>
  <main>
    <a class="backlink" href="../../roadmap.html">Voltar ao roadmap</a>
    <div
      class="node-context"
      data-node-position="true"
      data-level="basico"
      data-node-order="1"
      data-node-count="2"
      data-roadmap-slug="shape-fixture">
      <p><strong>Básico · 01 de 02</strong></p>
      <p>Roadmap: Shape Fixture</p>
      <p>Node atual: Primeiro node</p>
      <p>Anterior: início do roadmap · Próximo: <a href="../02-second-node/node.html">Segundo node</a></p>
    </div>
    <h1>Primeiro node</h1>
    <p class="lead">Abertura curta do node.</p>
    <section>
      <h2>Seção narrativa</h2>
      <p>Corpo narrativo.</p>
      <table>
        <tr><th>Conceito</th><th>Uso</th></tr>
        <tr><td>Campo</td><td>Exemplo narrativo permitido.</td></tr>
      </table>
    </section>
    <footer class="node-footer">
      <h2>Referências</h2>
      <ul class="reference-list">
        <li class="reference-item">
          <a href="https://example.com/source">Fonte primária</a>
          <span class="reference-note">Uso neste node: sustenta a explicação visível da fixture canônica.</span>
        </li>
      </ul>
    </footer>
  </main>
</body>
</html>
"""


def assert_pass(name: str, html: str) -> None:
    failures = collect_failures(html)
    if failures:
        raise AssertionError(f"{name} deveria passar: {failures}")


def assert_fails(name: str, html: str, expected_fragment: str) -> None:
    failures = collect_failures(html)
    if not any(expected_fragment in failure for failure in failures):
        raise AssertionError(
            f"{name} deveria falhar com {expected_fragment!r}; falhas: {failures}"
        )


def main() -> int:
    assert_pass("canonical", BASE_HTML)
    assert_fails(
        "multiple-root",
        BASE_HTML.replace("</style>", ":root { --late: #191919; }\n  </style>"),
        "exatamente um bloco :root",
    )
    assert_fails(
        "legacy-light-token",
        BASE_HTML.replace("--page: #191919;", "--page: #f8fafc;"),
        "token claro legado",
    )
    assert_fails(
        "label-canonico",
        BASE_HTML.replace("Node atual: Primeiro node", "Node atual: Primeiro node · Label canônico: Primeiro node"),
        "Label canônico",
    )
    assert_fails(
        "visible-node-id",
        BASE_HTML.replace("<h1>Primeiro node</h1>", "<p class=\"meta\">Node ID: <code>basico/01-first-node</code></p><h1>Primeiro node</h1>"),
        "Node ID",
    )
    assert_fails(
        "generic-boundary",
        BASE_HTML.replace("início do roadmap", "primeiro node do nível"),
        "primeiro node do nível",
    )
    assert_fails(
        "old-reference-title",
        BASE_HTML.replace("<footer class=\"node-footer\">", "<section><h2>Referências usadas</h2><p>Fonte antiga.</p></section><footer class=\"node-footer\">"),
        "título alternativo",
    )
    assert_fails(
        "reference-table",
        BASE_HTML.replace("<footer class=\"node-footer\">", "<section><h2>Referências</h2><table><tr><td>Fonte</td></tr></table></section><footer class=\"node-footer\">"),
        "tabela no corpo",
    )
    assert_fails(
        "old-reference-class",
        BASE_HTML.replace("<section>", "<section class=\"references\">", 1),
        "classe de referência antiga",
    )
    assert_fails(
        "duplicate-terminal-divider",
        BASE_HTML.replace(".node-footer { margin: 0;", ".node-footer { border-top: 1px solid var(--border); margin: 0;"),
        "divisor terminal duplicado",
    )
    assert_fails(
        "missing-footer",
        BASE_HTML.replace("<footer class=\"node-footer\">", "<section>").replace("</footer>", "</section>"),
        "footer.node-footer",
    )
    assert_fails(
        "unaccented-visible-ptbr",
        BASE_HTML.replace("Abertura curta do node.", "A pagina nao tem documentacao."),
        "texto visível sem acentuação",
    )
    assert_pass(
        "unaccented-technical-code",
        BASE_HTML.replace(
            "Corpo narrativo.",
            "Corpo narrativo. <code>nao documentacao</code>",
        ),
    )
    print("passa: shape validator cobre shell, contexto, root, referências e divisores")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
