# Guardrail 02 - Contratos dos Nodes

Cada node do roadmap deve ser suficiente para orientar `node-pages`.

## Checks

- slug `NN-slug`;
- level `basico`, `intermediario` ou `avancado`;
- `node_id` no formato `<level>/<slug>`;
- ordem local dentro do nível;
- label humano;
- papel na corrente local e no conjunto tri-level;
- pré-requisitos herdados;
- conceitos introduzidos pela primeira vez;
- escopo positivo denso;
- escopo negativo útil;
- perguntas concretas;
- vocabulário conceitual;
- exemplos e diagramas permitidos;
- armadilhas;
- critério de domínio;
- handoff;
- referências específicas.

O JSON e o HTML devem carregar o mesmo contrato essencial. A unicidade mecânica
do node é `node_id`, não o slug local isolado.
