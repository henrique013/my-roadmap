# Auditoria de escolha de primitivas visuais

Status geral: passa

## Base auditada

- HTML: `node.html`
- Dump: `research-dump.md`
- Ledger: `.editorial/concept-ledger.md`
- Texto visível: `.editorial/pipeline/01-visible-text/visible-text.md`
- Auditoria de exemplos: `.editorial/pipeline/03-example-sufficiency/example-audit.md`

## Resultado

| Relação visual | Primitiva escolhida | Status | Evidência |
|---|---|---|---|
| fronteira AE vs DLX | componente HTML/CSS em duas colunas | passa | Usa `.boundary-grid` e `.state-card`; não usa ASCII. |
| gatilhos de dead-lettering | cards HTML/CSS | passa | Usa `.trigger-grid` com quatro causas convergentes. |
| destinos depois da DLX | cards HTML/CSS | passa | Usa `.destination-grid` para quarentena, retry e loop sem dono. |
| retry com atraso | fluxo HTML/CSS | passa | Usa `.flow-line` e `.route-step`; não usa `<pre>` como diagrama. |
| forma mínima de configuração | `<pre><code>` | passa | Conteúdo é recorte literal/conceitual de configuração, com highlight semântico. |

## Checks de largura de conteúdo

| Check | Status | Evidência |
|---|---|---|
| parágrafos comuns ocupam a largura útil | passa | CSS define `p, ul, ol, .lead, .callout { max-width: none; }`. |
| callouts comuns ocupam a largura útil | passa | `.callout` não cria largura própria estreita. |
| nenhuma coluna textual estreita sem motivo | passa | Largura é controlada por `main`; grids são componentes estruturais. |

## Observações

- Não há ASCII excepcional.
- `pre code` redefine fundo, borda, padding e raio para evitar herança visual de inline `code`.
- Snippet técnico tem highlight semântico com classes `syntax-*`.
