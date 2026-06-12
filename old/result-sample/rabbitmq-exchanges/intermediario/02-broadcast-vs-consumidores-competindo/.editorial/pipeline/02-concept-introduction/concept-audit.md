# Auditoria de introdução conceitual

Status geral: passa

## Base auditada

- HTML: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/node.html`
- Texto visível: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/.editorial/pipeline/01-visible-text/visible-text.md`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/.editorial/concept-ledger.md`
- Rodada: 2026-06-10, após extração mecânica e scanner literal de aliases bloqueados.

## Primeiras ocorrências

| Conceito | Primeira ocorrência visível | Status | Evidência |
|---|---|---|---|
| Cópia por fila | Seção "O evento precisa existir em mais de um lugar" e visual seguinte | passa | A narrativa mostra e-mail, auditoria e analytics antes de nomear a cópia por fila. |
| Broadcast | Lead e seção "A cópia nasce na fila..." | passa | O lead já carrega a explicação mínima: papéis diferentes multiplicam filas; o corpo reforça antes de aprofundar. |
| Consumidores competindo | Lead e seção "Workers equivalentes..." | passa | O lead contrasta com instâncias equivalentes e a seção prepara workers do mesmo papel antes do nome. |
| Grupo de consumidores | Tabela e seção de workers | passa | Aparece depois da explicação de fila compartilhada por instâncias equivalentes. |
| Prefetch | Seção "A janela de entregas..." | passa | Antes do termo, o texto explica entregas em andamento ainda não confirmadas. |
| Consumer capacity | Visual da janela e parágrafo próximo | passa | Aparece como sinal de capacidade da fila entregar imediatamente, não como regra de topologia. |
| Fanout | Seção "A cópia nasce..." | passa | Aparece depois de broadcast e cópia por fila; não reensina tipos clássicos. |
| Direct e topic | Seção "A cópia nasce..." | passa | Aparecem apenas como nota curta de múltiplos bindings compatíveis. |

## Aliases e conceitos reservados

- Scanner literal de aliases bloqueados: passa.
- O label real do próximo node aparece em `.node-context` por contrato de navegação. O ledger não o bloqueia literalmente porque essa ocorrência é orientação de posição, não explicação narrativa.
- O corpo não usa os conceitos reservados a nodes futuros como base da explicação.

## Avaliação narrativa

- O HTML abre por situação concreta, não por lista de erros.
- O contraste corretivo aparece depois que os dois modelos positivos foram construídos.
- Títulos não copiam as seções do dump.
- O texto não expõe `node_id`, slug ou metadados técnicos fora de atributos e caminhos internos.

## Resultado

Status: passa. Nenhuma reescrita conceitual obrigatória.
