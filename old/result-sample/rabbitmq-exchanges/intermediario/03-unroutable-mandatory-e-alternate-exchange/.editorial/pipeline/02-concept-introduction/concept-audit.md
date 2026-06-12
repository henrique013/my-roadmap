# Concept introduction audit

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

## Primeiras ocorrências

| Conceito | Primeira ocorrência relevante | Preparação | Status |
|---|---:|---|---|
| Mensagem sem rota | 13 | A abertura mostra exchange existente, key nova e ausência de binding antes de nomear a falha. | passa |
| `mandatory` | 22 | O fluxo já mostrou publicação sem rota e caminho sem pedido de retorno antes da flag aparecer. | passa |
| Retorno ao publisher | 24 | O visual introduz a necessidade de sinal ao publisher antes do termo e a seção seguinte aprofunda. | passa |
| `basic.return` | 32 | A seção já explicou `mandatory` como pedido de retorno antes de nomear o método. | passa |
| Alternate Exchange | 28 | O caminho de rota alternativa aparece depois de a rota principal falhar; a seção seguinte define AE. | passa |
| Roteamento de fallback | 29 | O fluxo visual prepara a ideia de caminho alternativo antes do termo abstrato. | passa |
| Handler de retorno | 32 | O texto já explicou que o broker devolve a mensagem ao publisher antes de exigir lógica de tratamento. | passa |

## Ocorrências de shell obrigatório

- O contexto de posição exibe o label canônico do node e o label real do próximo node por contrato da skill.
- Esses textos aparecem antes do corpo narrativo, mas não são usados como explicação do mecanismo.
- A preparação conceitual do capítulo começa no `h1` e no `lead`, sem depender desses labels como definição.

## Scanner literal

- Comando executado: `scan_blocked_terms.py --ledger ... --visible ...`
- Resultado: passa; nenhum termo bloqueado literal encontrado.

## Vazamentos encontrados

- Nenhum vazamento semântico relevante.
- Nenhum conceito reservado sustenta a explicação principal.
- A fronteira com evento em fila já roteada aparece apenas no encerramento e no visual de fronteira.

## Termos de fonte e referência

- Referências finais usam formas preparadas: Documentação de publishers, Documentação de Alternate Exchanges, Documentação de exchanges, Referência AMQP 0-9-1 e Documentação sobre acknowledgements e confirmações.
- A fonte de dead lettering fica somente no dump, sem link visível no HTML.

## Resultado da rodada

- HTML precisa reescrita: não
