# Example sufficiency audit

Status: passa

## Exemplos e suportes concretos

| Suporte | Status | Evidência |
|---|---|---|
| Exemplo condutor `events.public` | passa | O exemplo abre a página, volta no snippet, aparece no mapa topológico e sustenta a leitura de métricas. |
| Snippet conceitual de `exchange.bind` | passa | O bloco mostra forma e direção source -> destination, tem aviso de que não é comando operacional e não contém sequência executável. |
| Mapa source -> destination exchanges | passa | O visual HTML/CSS mostra `events.public` ligado a `orders.internal` e `audit.internal`, reduzindo abstração topológica. |
| Contraste E2E vs consumidor que republica | passa | A tabela aparece depois de o modelo positivo ser construído e separa roteamento do broker de responsabilidade de aplicação. |
| Roteamento transitivo e ciclos | passa | O componente HTML/CSS mostra convergência em uma fila e proteção contra ciclo sem virar laboratório. |
| Leitura de métrica de ingress | passa | Os cards de sinais mostram source, destination e filas finais sem abrir diagnóstico avançado. |

## Excesso evitado

- Não há roteiro de execução, client library, CLI ou sequência de comandos.
- Não há reensino de bindings básicos, tipos de exchange ou routing keys fora do necessário.
- Não há explicação de federation, WAN ou multi-cluster.
- Não há aula de observabilidade ou troubleshooting completo.

## Decisão

Os exemplos são suficientes para forma, topologia, contraste, estado e fronteira. Não há reescrita obrigatória por falta ou excesso de concretização.
