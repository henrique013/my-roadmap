# Pipeline de Qualidade do Roadmap

Este pipeline valida `roadmap.html` e `.roadmap/roadmap-contract.json` antes da
resposta final.

## Rodada Global

Execute:

```text
docker version
docker image inspect my-roadmap-roadmap-runtime:playwright-1.60.0
  |
gerar roadmap.html
gerar .roadmap/roadmap-contract.json
  |
  +-> 01-html-shape: validar estrutura do HTML
  +-> 02-contract-schema: validar JSON contra schema versionado
  +-> 03-contract-consistency: validar coerência HTML <-> JSON, níveis, nodes e anti-repetição global
  +-> 04-source-coverage: validar fontes e referências
  +-> 05-visual-render: renderizar desktop/mobile
  +-> corrigir e repetir até ponto fixo
```

## Saídas Internas

```text
.roadmap/roadmap-contract.json
.roadmap/pipeline/01-html-shape/html-shape-audit.md
.roadmap/pipeline/02-contract-schema/contract-schema-audit.md
.roadmap/pipeline/03-contract-consistency/contract-consistency-audit.md
.roadmap/pipeline/04-source-coverage/source-audit.md
.roadmap/pipeline/05-visual-render/visual-audit.md
.roadmap/pipeline/05-visual-render/render-checks.json
.roadmap/pipeline/05-visual-render/playwright/desktop.png
.roadmap/pipeline/05-visual-render/playwright/mobile.png
```

O schema versionado fica em
`roadmap-page/schema/roadmap-contract.schema.json`. Ele valida a forma mínima do
contrato; a coerência semântica entre HTML, níveis, `node_id`, slugs, ordem
local, fontes e anti-repetição global continua no validador Python.

## Guardrails

1. Leia `01-roadmap-structure.md`.
2. Leia `02-node-contracts.md`.
3. Leia `03-anti-repetition.md`.
4. Leia `04-source-coverage.md`.
5. Leia `05-visual-render-audit.md`.

Use os scripts quando disponíveis:

```text
docker version
docker image inspect my-roadmap-roadmap-runtime:playwright-1.60.0

docker/runtime/run python3 <skill-dir>/roadmap-page/scripts/check_roadmap_html_shape.py \
  --html <roadmap-dir>/roadmap.html

docker/runtime/run node <skill-dir>/roadmap-page/scripts/check_roadmap_visual_render.mjs \
  --roadmap-dir <roadmap-dir>

docker/runtime/run python3 <skill-dir>/roadmap-page/scripts/validate_roadmap_artifacts.py \
  --roadmap-dir <roadmap-dir>
```

O diagnóstico Docker deve acontecer antes de criar artefatos. O wrapper não
constrói imagem; se o runtime Docker ou a imagem local não estiverem prontos,
bloqueie e oriente o build Docker explícito. O validador final de artefatos
roda depois do Playwright porque também confere as evidências renderizadas.

Se qualquer guardrail reescrever HTML, JSON ou CSS, reinicie a rodada.

## Ponto Fixo

Ponto fixo só existe quando:

- `roadmap.html` e `roadmap-contract.json` correspondem à última versão;
- `roadmap-contract.json` passa no schema versionado;
- os nodes do HTML e do JSON têm os mesmos níveis, `node_id`, slugs e ordem
  local;
- nenhum nível tem mais de 10 nodes;
- fontes e anti-repetição global estão rastreáveis por `node_id`;
- as auditorias dos pipes `01`, `02`, `03`, `04` e `05` registram passagem;
- mapas, fluxos e sequências visuais não usam `<pre>` como atalho;
- a auditoria visual renderizada registra `Status geral: passa`;
- não há overflow horizontal global;
- texto comum não está artificialmente estreito;
- a resposta final não expõe artefatos internos.
