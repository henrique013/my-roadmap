# Pipeline de Qualidade do Roadmap

Este pipeline valida `roadmap.html` e `.roadmap/roadmap-contract.json` antes da
resposta final.

## Rodada Global

Execute:

```text
gerar roadmap.html
gerar .roadmap/roadmap-contract.json
  |
  +-> validar estrutura do HTML
  +-> validar coerência HTML <-> JSON
  +-> validar contratos dos nodes
  +-> validar anti-repetição
  +-> validar fontes
  +-> validar primitiva visual de mapas, fluxos e sequências
  +-> renderizar desktop/mobile
  +-> corrigir e repetir até ponto fixo
```

## Guardrails

1. Leia `01-roadmap-structure.md`.
2. Leia `02-node-contracts.md`.
3. Leia `03-anti-repetition.md`.
4. Leia `04-source-coverage.md`.
5. Leia `05-visual-render-audit.md`.

Use os scripts quando disponíveis:

```text
python3 templates/skills-local/roadmap/roadmap-page/scripts/check_roadmap_html_shape.py \
  --html <roadmap-dir>/roadmap.html

python3 templates/skills-local/roadmap/roadmap-page/scripts/validate_roadmap_artifacts.py \
  --roadmap-dir <roadmap-dir>

npm run roadmap:roadmap-visual-check -- \
  --html <roadmap-dir>/roadmap.html
```

Se qualquer guardrail reescrever HTML, JSON ou CSS, reinicie a rodada.

## Ponto Fixo

Ponto fixo só existe quando:

- `roadmap.html` e `roadmap-contract.json` correspondem à última versão;
- os nodes do HTML e do JSON têm mesma ordem e mesmos slugs;
- fontes e anti-repetição estão rastreáveis;
- mapas, fluxos e sequências visuais não usam `<pre>` como atalho;
- a auditoria visual renderizada registra `Status geral: passa`;
- não há overflow horizontal global;
- texto comum não está artificialmente estreito;
- a resposta final não expõe artefatos internos.
