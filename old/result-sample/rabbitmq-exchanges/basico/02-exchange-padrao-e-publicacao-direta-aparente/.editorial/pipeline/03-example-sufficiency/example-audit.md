# Example sufficiency audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Node: `basico/02-exchange-padrao-e-publicacao-direta-aparente`
- Rodada: 1
- Data: 2026-06-08
- HTML auditado: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/node.html`
- Visible text: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/.editorial/pipeline/01-visible-text/visible-text.md`
- Dump: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/research-dump.md`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/basico/02-exchange-padrao-e-publicacao-direta-aparente/.editorial/concept-ledger.md`

## Status geral

Status geral: passa

## Rubrica aplicada

- Exemplo obrigatório apenas quando reduz ambiguidade essencial.
- Excesso de exemplo também falha.
- Snippets, tabelas e visuais devem ser mínimos e dentro do escopo.

## Blocos auditados

| Ordem | Seção | Tipo de demanda | Suporte encontrado | Status | Ação |
|---:|---|---|---|---|---|
| 1 | O campo vazio que parece sumir | forma de campos | Snippet conceitual com `exchange_name` e `routing_key`, com leitura textual | passa | Nenhuma |
| 2 | A ligação que o broker já criou | ordem e estado | Componente HTML/CSS mostrando publisher, default exchange, ligação automática e fila | passa | Nenhuma |
| 3 | Por que isso é útil, e onde parar | contraste | Cards e tabela comparando default exchange e direct exchange própria | passa | Nenhuma |
| 4 | A exchange especial não é uma exchange comum | fronteira | Callout curto sobre `""` e `amq.default` | passa | Nenhuma |
| 5 | Referências usadas | rastreabilidade | Tabela curta de fontes e uso | passa | Nenhuma |

## Falhas

- Nenhuma.

## Excesso detectado

- Nenhum. O HTML não usa comandos, conexão, imports, declaração de fila ou sequência operacional.
- O exemplo `task_queue` não repete o exemplo `pedido.criado` do node anterior.

## Resultado da rodada

- HTML precisa reescrita: não.
