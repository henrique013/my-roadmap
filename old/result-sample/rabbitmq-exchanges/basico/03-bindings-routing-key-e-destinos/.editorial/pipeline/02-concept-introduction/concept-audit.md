# Auditoria de introdução conceitual

## Status

Status geral: passa

## Escopo auditado

- Arquivo auditado: `node.html`
- Texto visível usado: `.editorial/pipeline/01-visible-text/visible-text.md`
- Ledger usado: `.editorial/concept-ledger.md`
- Dump usado: `research-dump.md`
- Node: `basico/03-bindings-routing-key-e-destinos`
- Rodada: final

## Resultado por conceito

| Conceito | Status | Evidência |
|---|---|---|
| Tabela de roteamento vazia | passa | A abertura mostra `orders.events` sem regras antes de nomear o estado como tabela vazia. |
| Binding | passa | O termo é nomeado depois de explicar a linha que cria uma saída da exchange. |
| Routing key | passa | Aparece no lead e é recontextualizada como valor da publicação antes de contrastar com a regra. |
| Binding key | passa | Só aparece depois de binding e routing key estarem separados. |
| Source exchange | passa | Surge na leitura da forma do binding, depois de a direção da regra estar preparada. |
| Destination e destination type | passa | O HTML primeiro apresenta a saída do binding e depois classifica queue, stream ou exchange. |
| Binding arguments | passa | Aparecem no snippet e na tabela como parâmetros opcionais da regra, não como payload. |
| Zero, uma ou várias rotas | passa | A explicação vem depois da avaliação de bindings e não entra em tratamento operacional. |

## Aliases e termos reservados

- `scan_blocked_terms.py`: passa, nenhum termo bloqueado literal encontrado.
- O label do próximo node aparece no contexto de navegação por contrato de posição e não sustenta a explicação do corpo.
- Termos reservados a `mandatory`, alternate exchange, headers e E2E não aparecem como vocabulário pedagógico no HTML.

## Primeiras ocorrências

| Termo | Primeira ocorrência aceitável | Decisão |
|---|---|---|
| `orders.created` | Exemplo condutor no lead | passa |
| `binding` | Depois do contraste entre tabela sem saídas e linhas de saída | passa |
| `routing key` | Lead e seção da publicação, com explicação local | passa |
| `binding key` | Depois de routing key e binding estarem preparados | passa |
| `arguments` | Snippet conceitual e tabela de campos | passa |

## Fronteiras

- A página menciona que o tipo da exchange decide como key e argumentos participam, mas não detalha os tipos.
- A página fala de ausência de destino inicial, mas não usa termos operacionais reservados.
- A página cita `exchange` como destination type, mas não aprofunda bindings entre exchanges.

## Conclusão

Status: passa. O HTML prepara os conceitos antes do uso e mantém os tópicos futuros como fronteira.
