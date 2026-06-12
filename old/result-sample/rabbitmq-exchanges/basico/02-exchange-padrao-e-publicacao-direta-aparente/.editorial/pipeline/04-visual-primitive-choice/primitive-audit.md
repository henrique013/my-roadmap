# Visual primitive choice audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Node: `basico/02-exchange-padrao-e-publicacao-direta-aparente`
- Rodada: 1
- Data: 2026-06-08
- HTML auditado: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/node.html`

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidência |
|---|---|---|
| primitiva visual adequada ao conceito | passa | Fluxo da default exchange usa componente HTML/CSS; contraste usa cards e tabela. |
| exceções ASCII justificadas | passa | Nenhuma exceção ASCII foi usada. |
| nenhum `<pre>` usado como atalho visual | passa | O único `<pre>` é snippet literal de campos de publicação e possui highlight semântico. |

## Suportes auditados

| Suporte | O que mostra | Primitiva | Status |
|---|---|---|---|
| Snippet de campos | Forma literal de `exchange_name` e `routing_key` | `<pre><code>` com `syntax-*` | passa |
| Fluxo pela default exchange | Ordem e estado da publicação até a fila | HTML/CSS `.route-diagram` e `.flow-step` | passa |
| Comparação default/direct própria | Contraste de intenção e custo conceitual | Cards e tabela | passa |
| Fronteira `""` / `amq.default` | Limite de nome | Callout | passa |

## Resultado da rodada

- HTML precisa reescrita: não.
