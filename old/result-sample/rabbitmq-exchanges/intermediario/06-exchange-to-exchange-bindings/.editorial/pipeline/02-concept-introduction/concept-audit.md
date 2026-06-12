# Concept introduction audit

Status: passa

## Escopo auditado

- HTML: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/06-exchange-to-exchange-bindings/node.html`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/06-exchange-to-exchange-bindings/.editorial/concept-ledger.md`
- Texto visível: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/06-exchange-to-exchange-bindings/.editorial/pipeline/01-visible-text/visible-text.md`

## Primeiras ocorrências

| Conceito | Status | Evidência |
|---|---|---|
| Exchange-to-exchange binding | passa | O título carrega o label canônico; no corpo, a página primeiro mostra a necessidade de uma exchange apontar para outra antes de nomear E2E. |
| Source exchange | passa | Aparece depois de a direção da aresta ser explicada como o ponto onde a mensagem entra no trecho. |
| Destination exchange | passa | Aparece junto da explicação de que a segunda exchange continua roteando, sem ser tratada como fila final. |
| `exchange.bind` | passa | Só aparece após source/destination estarem definidos e é mostrado em snippet conceitual não executável. |
| Roteamento transitivo | passa | Aparece depois do exemplo com `events.public`, `orders.internal` e `audit.internal`. |
| Detecção de ciclos | passa | Aparece depois de roteamento transitivo e é tratada como proteção do broker, não como recomendação de desenho. |
| Métrica de ingress da exchange destino | passa | Aparece depois de a página explicar que E2E não republica a mensagem. |

## Termos bloqueados

O script `scan_blocked_terms.py` passou sem candidatos literais no texto visível. A leitura semântica também não encontrou vazamento de federation, multi-cluster, WAN, troubleshooting avançado ou implementação por client library.

## Risco de tom corretivo

Status: passa. A narrativa começa com uma situação de composição de topologia, constrói o modelo positivo de source/destination e só depois introduz contrastes com republicação, ciclos e métricas.

## Revisão incorporada

A faixa inicial de tags foi ajustada após revisão read-only para não antecipar `roteamento transitivo`, `source exchange` ou `destination exchange` antes da preparação conceitual.

## Decisão

Não há reescrita obrigatória por introdução conceitual.
