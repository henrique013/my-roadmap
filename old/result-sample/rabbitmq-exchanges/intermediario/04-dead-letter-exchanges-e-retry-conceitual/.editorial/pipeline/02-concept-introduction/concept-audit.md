# Auditoria de introdução conceitual

Status geral: passa

## Base auditada

- HTML: `node.html`
- Dump: `research-dump.md`
- Ledger: `.editorial/concept-ledger.md`
- Texto visível: `.editorial/pipeline/01-visible-text/visible-text.md`

## Resultado

| Check | Status | Evidência |
|---|---|---|
| contexto de posição usa label contratual | passa | `Dead Letter Exchanges e retry conceitual` aparece no `.node-context` por contrato do node. |
| fronteira AE vs DLX é preparada antes do corpo técnico | passa | A abertura separa falha de rota inicial de saída posterior da fila. |
| Dead Letter Exchange é nomeada no corpo depois da situação | passa | O texto primeiro mostra mensagem já na fila e decisão de saída; depois nomeia DLX. |
| negative acknowledgement e `requeue` são preparados | passa | A seção do consumer explica entrega não concluída antes de citar `requeue=true` e `requeue=false`. |
| TTL, limite de fila e delivery limit não vazam cedo | passa | Esses termos aparecem só depois que dead-lettering já foi introduzido. |
| concepts reservados não sustentam a explicação | passa | `x-death`, counters avançados, at-least-once dead-lettering e detalhes de permissões não aparecem no HTML. |
| referências finais não introduzem conceito proibido | passa | Os títulos visíveis foram adaptados para os conceitos já preparados no corpo. |

## Observações

- A ocorrência antecipada de `Policies, x-arguments e permissões` está restrita ao label do próximo node no contexto de posição e ao handoff final permitido.
- A página constrói o modelo positivo antes de alertar sobre loops de retry.
