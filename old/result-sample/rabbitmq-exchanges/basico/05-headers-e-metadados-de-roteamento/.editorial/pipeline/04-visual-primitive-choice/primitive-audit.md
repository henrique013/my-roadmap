# Visual primitive choice audit

## Metadados

- Roadmap: rabbitmq-exchanges
- Level: basico
- Node: 05-headers-e-metadados-de-roteamento
- Node ID: basico/05-headers-e-metadados-de-roteamento
- Data: 2026-06-08
- Insumos: `research-dump.md`, `.editorial/concept-ledger.md`, `node.html`, `visible-text.md`

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidencia |
|---|---|---|
| visual conceitual usa HTML/CSS, nao ASCII | passa | `message-map`, `match-flow` e `compare-grid` sao componentes estruturados |
| snippet literal e apropriado | passa | o bloco `pre` mostra argumentos conceituais de binding, com highlight semantico |
| tabelas sao usadas para comparacao tabular real | passa | tabela de `x-match` e tabela de escolha topic/headers |
| nao ha `<pre>` usado como diagrama | passa | unico `pre` e formato literal de argumentos |
| largura de texto respeita contrato visual | passa | `p`, `.lead` e `.callout` nao criam coluna artificial estreita |
| tema `notion-dark` preservado | passa | CSS usa superficies escuras e tokens semanticos |

## Decisoes de primitiva

| Necessidade | Primitiva | Resultado |
|---|---|---|
| separar routing key, headers e payload | componente HTML/CSS | passa |
| comparar binding e mensagem | componente HTML/CSS | passa |
| explicar `x-match` | tabela + snippet literal | passa |
| comparar topic e headers | cards + tabela | passa |

## Resultado da rodada

- HTML precisa reescrita: não
- Nenhuma reescrita é obrigatória.
