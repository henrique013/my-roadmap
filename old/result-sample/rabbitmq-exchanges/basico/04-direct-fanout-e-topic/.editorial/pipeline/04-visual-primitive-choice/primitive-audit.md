# Primitive choice audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Node: `basico/04-direct-fanout-e-topic`
- Rodada: 1
- Data: 2026-06-08
- HTML auditado: `node.html`
- Dump: `research-dump.md`
- Ledger: `.editorial/concept-ledger.md`

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidência |
|---|---|---|
| primitiva visual adequada ao conceito | passa | Contrastes de direct/fanout/topic, cardinalidade de direct e segmentos de topic usam HTML/CSS semântico. |
| exceções ASCII justificadas | passa | Nenhuma exceção ASCII foi usada. |
| nenhum `<pre>` usado como atalho visual | passa | O único `<pre>` é snippet literal de padrões topic, com `<code>` e classes `syntax-*`. |

## Suportes concretos auditados

| Suporte | O que mostra | Primitiva | Status |
|---|---|---|---|
| Cards de decisão | contraste entre igualdade, cópia ampla e padrão por partes | componente HTML/CSS | passa |
| Visual de direct | publicação, bindings e destinos alcançados | componente HTML/CSS | passa |
| Tabela de fanout | consequência e fronteira de filtro | tabela | passa |
| Cards de segmentos | forma de routing key topic | componente HTML/CSS | passa |
| Snippet de topic | padrões literais com `*` e `#` | `<pre><code>` com highlight | passa |
| Tabela de escolha | intenção, tipo e cuidado | tabela | passa |

## Resultado da rodada

- HTML precisa reescrita: não

