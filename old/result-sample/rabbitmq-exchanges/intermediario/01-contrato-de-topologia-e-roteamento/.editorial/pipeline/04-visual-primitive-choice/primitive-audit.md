# Visual primitive choice audit

Status geral: passa

## Primitivas avaliadas

| Relação | Primitiva usada | Resultado | Justificativa |
|---|---|---|---|
| Quem conhece quem na topologia | HTML/CSS `.topology` | passa | Relação espacial entre producer, exchange e filas exige visual semântico. |
| Mudança de topologia sem alterar publisher | HTML/CSS `.state-grid` | passa | Estado antes/depois revela o que muda e o que permanece. |
| Comparação de recortes | Tabela | passa | O leitor já tem contexto antes da comparação; tabela consolida trade-offs. |
| Relação material entre exchange, filas e bindings | HTML/CSS `.content-grid` | passa | A demanda é conceitual e relacional, portanto cards são melhores que bloco literal. |

## ASCII e blocos literais

- Nenhum diagrama ASCII foi usado.
- Nenhum bloco `<pre>` foi usado.
- Visual conceitual simples foi implementado com HTML/CSS.

## Decisão

As primitivas são compatíveis com as demandas atualizadas do dump e do contrato visual. O HTML não precisa de reescrita.
