# Concept introduction audit

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
| contexto de posicao aparece antes da narrativa | passa | `node-context` contem nivel, posicao, roadmap, node atual, anterior e proximo |
| conceitos herdados sao usados sem redefinicao longa | passa | routing key, binding, direct, fanout e topic aparecem como prerequisitos herdados |
| atributos independentes sao preparados antes de headers exchange no corpo | passa | abertura mostra `tenant`, `format` e `priority` antes de nomear o mecanismo |
| message headers sao introduzidos como metadados separados do corpo | passa | primeira secao separa key, headers e payload |
| payload opaco aparece como fronteira depois de explicar headers | passa | visual e texto deixam o corpo fora da decisao de roteamento |
| `x-match` aparece depois da necessidade de combinar varios criterios | passa | secao pergunta se a exchange exige todos ou aceita qualquer criterio antes do nome |
| termos reservados a nodes futuros nao sustentam a explicacao | passa | fila, consumidor e entrega aparecem apenas no contexto de proximo node |
| fontes visiveis nao introduzem conceitos sem preparo | passa | referencias usam titulos tecnicos ja permitidos pelo ledger |

## Ocorrencias auditadas

| Conceito | Primeira ocorrencia relevante | Resultado |
|---|---|---|
| Headers exchange | titulo e label do node; no corpo apos atributos independentes | passa |
| Message headers | apos explicar mapa de metadados separado do corpo | passa |
| Payload opaco | no visual de fronteira entre headers e corpo | passa |
| Argumentos do binding | antes da tabela de comparacao binding/mensagem | passa |
| `x-match` | apos explicar ambiguidade todos/qualquer criterio | passa |
| `all`, `any`, `all-with-x`, `any-with-x` | tabela dedicada depois de `x-match` | passa |

## Termos bloqueados

- `scan_blocked_terms.py`: passa, nenhum termo bloqueado literal encontrado.
- Revisao semantica: nao ha abertura de serializers, policies, plugins, DLX, AE, mandatory, publisher confirms ou consumidores competindo.

## Resultado da rodada

- HTML precisa reescrita: não
- Nenhuma reescrita é obrigatória.
