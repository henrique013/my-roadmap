# Visual render audit

## Metadados

- Roadmap: rabbitmq-exchanges
- Level: basico
- Node: 03-bindings-routing-key-e-destinos
- Node ID: basico/03-bindings-routing-key-e-destinos
- Rodada: gerada pelo script Playwright
- Data: 2026-06-08T20:18:10.961Z
- HTML auditado: `node.html`
- Ferramenta: Playwright Library
- Browser: Chromium headless
- Viewports: desktop 1280x900, mobile 390x844
- Checks detalhados: `.editorial/pipeline/05-visual-render/render-checks.json`

## Evidências

| Viewport | Screenshot | Observações |
|---|---|---|
| desktop | `.editorial/pipeline/05-visual-render/playwright/desktop.png` | screenshot gerada |
| mobile | `.editorial/pipeline/05-visual-render/playwright/mobile.png` | screenshot gerada |

## Status geral

Status geral: passa

## Checks mecânicos

| Check | Status | Evidência |
|---|---|---|
| tema visual `notion-dark` aplicado | passa | marcador, color-scheme e superfícies escuras confirmados |
| raiz CSS escura única, sem legado claro | passa | marcador, color-scheme e superfícies escuras confirmados |
| `.node-context` usa estilo fixo | passa | estilos computados do contexto batem com o contrato |
| `.node-context a` usa estilo fixo | passa | links do contexto usam cor, peso e sublinhado fixos |
| `footer.node-footer` usa forma e estilo fixos | passa | rodapé e links do rodapé batem com o contrato |
| divisores terminais não duplicam o divisor canônico | passa | containers terminais não possuem border-top próprio |
| primitivas visuais fixas não derivam estilo próprio | passa | tags renderizam compactas e flow-step não desenha conector duplicado |
| `pre code` não herda chip de inline code | passa | estilos computados sem fundo, borda, padding ou raio próprios |
| snippets técnicos têm highlight semântico | passa | blocos técnicos usam classes de highlight ou são texto literal permitido |
| visuais conceituais não usam `<pre>` como atalho | passa | nenhum `<pre>` suspeito sem exceção ASCII explícita |
| contraste mínimo em texto e código | passa | amostras renderizadas com contraste >= 4.5:1 |
| página sem overflow horizontal global | passa | desktop e mobile sem overflow horizontal global |
| texto comum ocupa largura útil | passa | parágrafos, listas, lead e callouts comuns usam >= 90% da largura útil no desktop |
| mobile legível sem sobreposição óbvia | passa | sem overflow global; agente ainda deve inspecionar screenshot mobile |
| assets externos inesperados | passa | nenhuma requisição http(s) observada |
| auditoria sem placeholder manual | passa | campos de inspeção foram preenchidos com evidência concreta |

## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa | >= 90% da largura útil no desktop |
| callouts comuns ocupam a largura útil | passa | >= 90% da largura útil no desktop |
| nenhuma coluna textual estreita sem motivo | passa | nenhum bloco textual comum abaixo do limite |

## Inspeção visual do agente

- `.node-context`: estilo computado validado nos viewports desktop e mobile; screenshots salvas em `playwright/`.
- `footer.node-footer`: estilo computado validado nos viewports desktop e mobile; screenshots salvas em `playwright/`.
- Divisores: containers terminais sem `border-top` próprio quando os checks passam.
- Tema escuro: marcador `notion-dark`, `color-scheme` e superfícies escuras registrados em `render-checks.json`.
- Cores dos exemplos: contraste e superfícies amostrados pelo script; revisar falhas listadas abaixo se existirem.
- Leitura dos snippets: chips inline, blocos `pre code` e highlight semântico medidos pelo script.
- Hierarquia visual: screenshots desktop e mobile geradas para revisão visual da rodada.
- Problemas observados: nenhuma falha mecânica quando o status geral é `passa`; falhas específicas aparecem na seção Falhas.

## Falhas

Nenhuma falha mecânica detectada pelo script.

## Resultado da rodada

- HTML precisa reescrita: não
- Se sim, atualizar `.editorial/pipeline/05-visual-render/revision-plan.md` e reiniciar a rodada global depois da reescrita.
