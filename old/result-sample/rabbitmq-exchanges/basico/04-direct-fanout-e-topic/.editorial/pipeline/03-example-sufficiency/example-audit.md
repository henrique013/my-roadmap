# Example sufficiency audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Node: `basico/04-direct-fanout-e-topic`
- Rodada: 1
- Data: 2026-06-08
- HTML auditado: `node.html`
- Visible text: `.editorial/pipeline/01-visible-text/visible-text.md`
- Dump: `research-dump.md`
- Ledger: `.editorial/concept-ledger.md`

## Status geral

Status geral: passa

## Rubrica aplicada

- Exemplo obrigatório apenas quando reduz ambiguidade essencial.
- Excesso de exemplo também falha.
- Snippets, tabelas e visuais devem ser mínimos e dentro do escopo.

## Blocos auditados

| Ordem | Seção | Tipo de demanda | Suporte encontrado | Status | Ação |
|---:|---|---|---|---|---|
| 1 | A diferença está na pergunta que a exchange faz | contraste | Três cards HTML/CSS comparando igualdade, cópia ampla e padrão por partes. | passa | nenhuma |
| 2 | Direct resolve quando a etiqueta precisa bater | estado e cardinalidade | Visual HTML/CSS mostra publicação, bindings que combinam e duas filas alcançadas. | passa | nenhuma |
| 3 | Fanout resolve quando escolher não faz parte da intenção | contraste | Tabela curta mostra key ignorada, cópia para filas ligadas e fronteira com filtro. | passa | nenhuma |
| 4 | Topic entra quando a key vira uma frase curta | forma | Segmentos em cards e snippet mínimo com highlight para `audit.*.login`, `audit.#` e `orders.#`. | passa | nenhuma |
| 5 | Como escolher sem decorar tipo por tipo | comparação | Tabela de intenção, tipo, leitura da key e cuidado imediato. | passa | nenhuma |
| 6 | Referências usadas | rastreabilidade | Tabela de fontes com uso no node. | passa | nenhuma |

## Falhas

Nenhuma.

## Excesso detectado

Nenhum. O HTML não inclui comandos, laboratório, sequência executável nem catálogo extenso de padrões.

## Resultado da rodada

- HTML precisa reescrita: não

