# Guardrail 01 - Estrutura do Roadmap

Valide se `roadmap.html` está completo, autocontido e sem Markdown cru.

## Checks

- `<!doctype html>` no início.
- `html lang="pt-BR"`.
- `meta charset="utf-8"`.
- viewport.
- CSS embutido.
- `<title>` e `<h1>`.
- seções de visão geral, mapa tri-level, lista resumida navegável por nível, matriz
  anti-repetição global, checklist final e referências consolidadas;
- seções explícitas para `basico`, `intermediario` e `avancado`;
- nodes com `id` estável, `data-level`, `data-node-id` e `data-node-slug`;
- links internos da lista resumida para cada seção completa de node;
- nenhum `flow-steps` numérico-only usado como lista de nodes;
- links relativos para `node.html` apenas quando o arquivo existe.
- nenhuma seção prática proibida.
- nenhum fence Markdown cru.

Use:

```text
python3 templates/skills-local/roadmap/roadmap-page/scripts/check_roadmap_html_shape.py \
  --html <roadmap-dir>/roadmap.html
```
