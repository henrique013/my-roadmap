# Auditoria de suficiência de exemplos

Status geral: passa

## Base auditada

- HTML: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/node.html`
- Dump: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/research-dump.md`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/.editorial/concept-ledger.md`

## Exemplos usados

| Exemplo | Função didática | Status | Risco controlado |
|---|---|---|---|
| `pedido.criado` para e-mail, auditoria e analytics | Mostra papéis diferentes que precisam de cópias independentes. | passa | Não vira tutorial nem repete contrato de routing do node anterior. |
| `relatorio.gerar` para três workers equivalentes | Mostra uma fila compartilhada dividindo entregas. | passa | Não recomenda comandos nem uma configuração específica. |
| Janela conceitual de prefetch | Mostra entregas em andamento e espaço para novas entregas. | passa | Não recomenda valores e não entra em tuning. |

## Suficiência qualitativa

- O exemplo condutor aparece em mais de um bloco: primeiro como papéis independentes, depois como contraste com workers equivalentes.
- A tabela consolida a decisão depois que a narrativa já preparou os conceitos.
- Os visuais explicam forma, estado e contraste; não são ornamentais.
- Não há laboratório, sequência de comandos, desafio, exercício ou projeto final.
- Snippets técnicos não foram necessários; a página usa nomes conceituais e componentes HTML/CSS.

## Resultado

Status: passa. Nenhuma reescrita de exemplos é obrigatória.
