# Auditoria de suficiência de exemplos

## Status

Status geral: passa

## Escopo auditado

- Arquivo auditado: `node.html`
- Dump usado: `research-dump.md`
- Ledger usado: `.editorial/concept-ledger.md`
- Texto visível usado: `.editorial/pipeline/01-visible-text/visible-text.md`

## Exemplo condutor

O exemplo `orders.events` com publicação `orders.created` atravessa a página:

| Trecho | Função didática | Status |
|---|---|---|
| Abertura | Mostra exchange existente sem regras de saída | passa |
| Snippet conceitual | Separa routing key da publicação e binding key da regra | passa |
| Mapa de rotas | Mostra múltiplos destinos para a mesma publicação | passa |
| Tabela de campos | Consolida source, destination, destination type e arguments | passa |

## Obrigações de concretização do dump

| Obrigação | Implementação | Status |
|---|---|---|
| Contraste routing key versus binding key | Snippet conceitual e tabela curta | passa |
| Exchange sem bindings como tabela vazia | Estado antes/depois em HTML/CSS | passa |
| Uma publicação encontrando múltiplos destinos | Mapa de source, bindings e destinations | passa |
| Destination type | Tabela de campos com queue, stream e exchange | passa |

## Excesso e fronteira

- Não há laboratório, comando, endpoint ou sequência executável.
- O snippet é conceitual, com placeholders de topologia e sem dependência de linguagem cliente.
- A página não reusa o exemplo do node anterior baseado em default exchange e `task_queue`.
- A página não antecipa detalhes de tipos clássicos, headers, AE, `mandatory`, consumers ou E2E.

## Conclusão

Status: passa. Os exemplos reduzem ambiguidade real de forma, estado, ordem e contraste sem transformar o node em exercício.
