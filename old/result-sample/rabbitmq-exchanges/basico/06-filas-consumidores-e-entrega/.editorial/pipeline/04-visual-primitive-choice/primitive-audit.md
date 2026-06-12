# Visual primitive audit

## Status geral

Status geral: passa

## Evidência

- Estados de mensagem usam cards HTML/CSS em `.state-flow`, adequados para mostrar estado e ordem.
- Contraste entre workers na mesma fila e filas independentes usa painéis HTML/CSS em `.queue-contrast`, adequado para mostrar topologia simples.
- A consolidação de responsabilidades usa tabela curta, adequada para comparação depois da narrativa.
- Não há diagrama ASCII.
- Não há `<pre>` para visual conceitual.
- Não há snippet técnico, então não há necessidade de highlight semântico em bloco de código.

## Checks

| Check | Status | Evidência |
|---|---|---|
| Fluxo ou estado simples usa HTML/CSS | passa | `.state-flow` |
| Topologia simples usa HTML/CSS | passa | `.queue-contrast` |
| Tabela aparece depois de contexto suficiente | passa | seção de responsabilidade |
| ASCII excepcional ausente | passa | nenhum `<pre data-ascii-exception>` necessário |

## Resultado

Nenhuma reescrita obrigatória foi identificada neste guardrail.
