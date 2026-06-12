# Roadmap visual render audit

## Metadados

- Roadmap: rabbitmq-exchanges
- Rodada: gerada pelo script Playwright
- Data: 2026-06-09T15:03:57.832Z
- HTML auditado: `roadmap.html`
- Ferramenta: Playwright Library
- Browser: Chromium headless
- Viewports: desktop 1280x900, mobile 390x844
- Checks detalhados: `.roadmap/pipeline/05-visual-render/render-checks.json`

## Evidências

| Viewport | Screenshot | Observações |
|---|---|---|
| desktop | `.roadmap/pipeline/05-visual-render/playwright/desktop.png` | screenshot gerada |
| mobile | `.roadmap/pipeline/05-visual-render/playwright/mobile.png` | screenshot gerada |

## Status geral

Status geral: passa

## Checks mecânicos

| Check | Status | Evidência |
|---|---|---|
| tema visual `notion-dark` aplicado | passa | marcador, color-scheme e superfícies escuras confirmados |
| `pre code` não herda chip de inline code | passa | estilos computados sem fundo, borda, padding ou raio próprios |
| snippets técnicos têm highlight semântico | passa | blocos técnicos usam classes de highlight ou são texto literal permitido |
| tabelas usam superfície estruturada | passa | td usa superfície escura e th usa variação escura |
| contraste mínimo em texto e código | passa | amostras renderizadas com contraste >= 4.5:1 |
| visuais conceituais não usam `<pre>` como atalho | passa | nenhum <pre> suspeito sem exceção ASCII explícita |
| página sem overflow horizontal global | passa | desktop e mobile sem overflow global |
| assets externos inesperados | passa | nenhuma requisição http(s) observada |

## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa | parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop |
| callouts comuns ocupam a largura útil | passa | parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop |
| nenhuma coluna textual estreita sem motivo | passa | parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop |

## Inspeção visual do agente

- Hierarquia visual: screenshots geradas; o agente deve confirmar antes da entrega.
- Leitura mobile: screenshots geradas; o agente deve confirmar antes da entrega.
- Problemas observados: registrar aqui qualquer falha vista nas screenshots.

## Falhas

Nenhuma falha mecânica detectada pelo script.

## Resultado da rodada

- HTML precisa reescrita: não
- Se sim, corrigir `roadmap.html` ou CSS e reiniciar a rodada global.
