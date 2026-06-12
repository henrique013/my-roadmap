# Example sufficiency audit

## Metadados

- Roadmap: Exchanges no RabbitMQ
- Node: Unroutable, mandatory e Alternate Exchange
- Rodada: 2
- Data: 2026-06-10
- HTML auditado: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/node.html`
- Visible text: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/.editorial/pipeline/01-visible-text/visible-text.md`
- Dump: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/research-dump.md`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/03-unroutable-mandatory-e-alternate-exchange/.editorial/concept-ledger.md`

## Status geral

Status geral: passa

## Rubrica aplicada

- Exemplo obrigatório apenas quando reduz ambiguidade essencial.
- Excesso de exemplo também falha.
- Snippets, tabelas e visuais devem ser mínimos, conceituais e dentro do escopo.

## Blocos auditados

| Ordem | Seção | Tipo de demanda | Suporte encontrado | Status | Ação |
|---:|---|---|---|---|---|
| 1 | A key nova ainda não tem destino | forma e causa | Exemplo condutor `orders.created.v2` sem binding compatível. | passa | nenhuma |
| 2 | Três caminhos depois da tentativa de roteamento | ordem e contraste | Visual HTML/CSS com descarte, retorno e AE. | passa | nenhuma |
| 3 | O retorno só existe se alguém pediu para ouvir | forma de parâmetro | Snippet conceitual mínimo com `mandatory` na publicação e handler de retorno. | passa | nenhuma |
| 4 | A rota alternativa pertence à exchange | forma de configuração conceitual | Snippet conceitual mínimo com `alternate-exchange` como propriedade da exchange. | passa | nenhuma |
| 5 | Escolher sinal, fallback ou os dois | comparação | Tabela curta de mecanismo, sinal, destino e risco. | passa | nenhuma |
| 6 | O limite está antes da fila | fronteira | Estado lado a lado entre falha de rota inicial e evento em fila já roteada. | passa | nenhuma |

## Falhas

- Nenhuma.

## Excesso detectado

- Nenhum. Os exemplos não formam roteiro executável, não usam comandos e não invadem tuning, policies, DLX ou confirms.

## Resultado da rodada

- HTML precisa reescrita: não
