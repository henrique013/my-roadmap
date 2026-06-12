# Concept introduction audit

Status geral: passa

## Escopo auditado

- HTML: `node.html`
- Dump: `research-dump.md`
- Ledger: `.editorial/concept-ledger.md`
- Texto extraído: `.editorial/pipeline/01-visible-text/visible-text.md`

## Primeiras ocorrências relevantes

| Conceito | Primeira ocorrência visível | Resultado | Evidência |
|---|---:|---|---|
| Contrato de publicação | 14 | passa | A abertura já estabeleceu producer, exchange, routing key e filas antes da nomeação. |
| Convenção de routing key | 29 | passa | `orders.created` aparece antes como intenção de publicação; a convenção é nomeada depois. |
| Fronteira publisher-topology-consumer | 80 | passa | A página já mostrou quem conhece exchange/key, bindings e filas internas. |
| Ownership de exchange | 102 | passa | O recorte de exchange e a responsabilidade semântica foram preparados antes. |
| Definitions como forma de topologia | 106 e referências | passa | Antes do snippet, a página explica exchanges, filas e bindings como peças explícitas da topologia. |

## Alias e termos reservados

- `scan_blocked_terms.py`: passa; nenhum termo bloqueado literal encontrado.
- O label do próximo node aparece no contexto de posição por exigência do contrato e não sustenta explicação prematura.
- Não há uso visível de permissions, policies, alternate exchange, DLX, confirms, E2E ou topologia multi-cluster.

## Decisão

Os conceitos do node são introduzidos por situação, consequência e visual antes de virarem vocabulário técnico. O HTML não precisa de reescrita.
