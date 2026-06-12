# Concept introduction audit

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

## Texto visível

- A extração contém `title`, backlink, contexto de posição, H1, lead, headings, tabelas, links, texto do snippet e `aria-label` do visual.
- A ordem de aparição preserva a sequência de leitura do HTML.
- O scanner literal de termos bloqueados passou sem candidatos.

## Primeiras ocorrências auditadas

| Conceito | Primeira ocorrência relevante | Status | Evidência |
|---|---|---|---|
| Exchange padrão / default exchange | `title` e H1 como label do node; corpo no parágrafo "exchange que o broker já traz pronta" | passa | O corpo prepara a ideia antes de depender do nome. |
| Nome vazio | lead com `exchange=""`; corpo em "campo de exchange sem nenhum caractere" | passa | A ocorrência inicial é material observado da API e é explicada imediatamente. |
| Routing key como nome da fila | lead/snippet como campo observado; explicação no bloco "Leitura segura" | passa | O texto diz que ela carrega o nome da fila apenas neste caso específico. |
| Binding automático | seção "A ligação que o broker já criou" | passa | Antes do termo, o texto explica que RabbitMQ liga a fila à default exchange ao declarar a fila. |
| Publicação direta aparente | title/H1 como label; corpo depois do fluxo | passa | O HTML nomeia a aparência depois de mostrar a rota pela default exchange. |
| Direct exchange própria | tabela e card de decisão após default exchange | passa | É apresentada só como alternativa explícita, sem ensinar tipos. |
| `amq.default` | callout "Fronteira de nome" | passa | Aparece depois do nome vazio e sem discutir permissões ou governança. |
| `task_queue` | lead e visual como exemplo condutor | passa | O texto a apresenta como fila simples para ler o mecanismo. |

## Vazamentos encontrados

- Nenhum termo bloqueado literal foi encontrado.
- Nenhum alias semântico de `mandatory`, AE, confirms, permissões, binding key detalhada, fanout/topic/headers ou contrato de topologia sustenta a explicação.

## Termos de fonte e referência

- Os links finais aparecem depois que `exchange`, default exchange, publicação e routing key já foram preparados.
- `RabbitMQ - Publishers` aparece apenas como fonte; não introduz confirms.
- `RabbitMQ - Hello World tutorial` aparece como fonte para forma dos campos; o HTML não vira tutorial.

## Conceitos reservados a nodes futuros

- `basico/03-bindings-routing-key-e-destinos`: o label do próximo node aparece no contexto de posição por contrato; o corpo não aprofunda binding key, source ou destination.
- `basico/04-direct-fanout-e-topic`: o HTML menciona direct exchange própria apenas como contraste curto e não abre fanout/topic.
- `intermediario/03-unroutable-mandatory-e-alternate-exchange`: não há discussão de mensagem sem rota, `mandatory`, retorno ou AE.
- `intermediario/05-policies-x-arguments-e-permissoes`: não há discussão de permissões ou governança.

## Resultado da rodada

- HTML precisa reescrita: não.
