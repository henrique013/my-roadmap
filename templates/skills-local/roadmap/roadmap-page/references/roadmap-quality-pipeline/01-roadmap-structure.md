# Guardrail 01 - Estrutura do Roadmap

Valide se `roadmap.html` está completo, autocontido e sem Markdown cru.

## Checks

- `<!doctype html>` no início.
- `html lang="pt-BR"`.
- `meta charset="utf-8"`.
- viewport.
- CSS embutido.
- `<title>` e `<h1>`.
- seções de visão geral, corrente de nodes, lista resumida, matriz
  anti-repetição, checklist final e referências consolidadas.
- nenhuma seção prática proibida.
- nenhum fence Markdown cru.

Use:

```text
python3 templates/skills-local/roadmap/roadmap-page/scripts/check_roadmap_html_shape.py \
  --html <roadmap-dir>/roadmap.html
```
