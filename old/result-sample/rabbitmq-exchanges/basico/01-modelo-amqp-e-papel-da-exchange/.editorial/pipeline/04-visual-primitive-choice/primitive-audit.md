# Visual primitive choice audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `01-modelo-amqp-e-papel-da-exchange`
- HTML auditado: `node.html`
- Data: 2026-06-08

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidência |
|---|---|---|
| fluxo conceitual usa HTML/CSS | passa | O caminho da mensagem usa `.path-diagram`, `.flow-row`, `.flow-step`, `.queue-card` e `.consumer-card`. |
| estados comparativos usam componente visual | passa | Zero/uma/várias filas usam `.result-grid` e cards, não `<pre>`. |
| fronteira de responsabilidades usa cards semânticos | passa | Exchange, fila e consumer usam `.responsibility-map`. |
| `<pre>` não é usado como atalho visual | passa | O HTML não contém blocos `<pre>`. |
| tabela é usada para mapeamento, não para substituir narrativa | passa | A tabela final mapeia pergunta, peça e leitura segura depois da explicação principal. |
| visuais são instrutivos, não decorativos | passa | Cada visual corresponde a obrigação didática registrada no dump. |

## Decisão

Nenhuma reescrita é obrigatória.
