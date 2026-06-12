# Auditoria de escolha de primitiva visual

Status geral: passa

## Base auditada

- HTML: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/node.html`
- Dump: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/02-broadcast-vs-consumidores-competindo/research-dump.md`

## Primitivas avaliadas

| Relação | Primitiva usada | Status | Evidência |
|---|---|---|---|
| Cópia por fila vs workers equivalentes | Componente HTML/CSS em duas colunas | passa | Mostra onde a multiplicação acontece: antes da fila ou dentro da fila. |
| Janela de prefetch | Componente HTML/CSS com slots | passa | Mostra estado cheio, espaço livre e sinal de capacidade. |
| Decisão por papel de consumo | Cards em grade | passa | Consolida pergunta decisória depois da explicação. |
| Comparação de intenção, desenho e consequência | Tabela | passa | A tabela aparece após o modelo narrativo e serve como consolidação. |

## Checks

- Nenhum visual conceitual simples usa `<pre>`.
- Não há ASCII excepcional.
- Não há bloco de código; portanto não há snippet monocromático a justificar.
- Componentes usam superfícies escuras, bordas semânticas e não criam coluna textual estreita.

## Resultado

Status: passa. Nenhuma reescrita de primitiva visual é obrigatória.
