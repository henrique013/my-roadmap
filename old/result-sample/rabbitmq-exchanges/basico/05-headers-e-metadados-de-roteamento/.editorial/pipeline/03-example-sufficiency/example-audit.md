# Example sufficiency audit

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
| exemplo condutor pequeno e recorrente | passa | `tenant=acme`, `format=pdf`, `priority=high` aparece na abertura, visual, tabela e snippet |
| exemplo nao vira laboratorio | passa | nao ha comandos, setup, cliente de linguagem ou exercicio |
| comparacao com topic e suficiente e limitada | passa | contraste usa `audit.user.login` apenas para distinguir hierarquia textual de atributos independentes |
| payload opaco tem fronteira concreta | passa | visual separa routing key, headers e payload |
| `x-match` tem suporte concreto suficiente | passa | tabela diferencia as quatro variantes e snippet mostra forma minima do binding |
| exemplos nao repetem o node 04 como eixo principal | passa | node 04 e usado apenas como contraste herdado, sem reensinar direct/fanout/topic |
| riscos aparecem como consequencia, nao como lista corretiva | passa | callout final trata padronizacao e sensibilidade dos headers sem dominar a narrativa |

## Suficiencia por trecho

| Trecho | Suporte concreto | Resultado |
|---|---|---|
| fronteira key/headers/payload | componente HTML/CSS em tres zonas | passa |
| match entre binding e mensagem | componente HTML/CSS com pares nome/valor | passa |
| `x-match` | tabela + snippet minimo com highlight | passa |
| topic versus headers | cards + tabela curta de decisao | passa |

## Resultado da rodada

- HTML precisa reescrita: não
- Nenhuma reescrita é obrigatória.
