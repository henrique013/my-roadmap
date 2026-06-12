# Visual primitive audit

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Node: Unroutable, mandatory e Alternate Exchange
- Rodada: 2
- Data: 2026-06-10
- HTML auditado: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/node.html`
- Dump: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/research-dump.md`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/.editorial/concept-ledger.md`

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidência |
|---|---|---|
| primitiva visual adequada ao conceito | passa | Fluxo de três caminhos e fronteira de estados usam componentes HTML/CSS; comparação usa tabela. |
| exceções ASCII justificadas | passa | Nenhum ASCII excepcional foi usado. |
| nenhum `<pre>` usado como atalho visual | passa | Os dois `<pre>` são snippets literais conceituais com campos, não diagramas, fluxos ou topologias. |
| snippets técnicos têm highlight semântico | passa | Snippets usam classes `syntax-key`, `syntax-op`, `syntax-value` e `syntax-comment`. |
| suporte concreto corresponde ao dump | passa | As três obrigações de concretização do dump aparecem como visual de fluxo, tabela e snippets mínimos. |

## Resultado da rodada

- HTML precisa reescrita: não
