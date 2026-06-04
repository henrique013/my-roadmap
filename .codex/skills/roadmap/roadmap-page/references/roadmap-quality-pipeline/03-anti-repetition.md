# Guardrail 03 - Anti-Repetição

Repetição é defeito estrutural do roadmap.

## Checks

- matriz anti-repetição existe no HTML;
- `anti_repetition` existe no JSON;
- cada conceito central tem `node_id` de primeira introdução;
- a matriz cobre fronteiras entre `basico`, `intermediario` e `avancado`;
- retomadas permitidas são lembretes, pré-requisitos ou nova camada
  justificada;
- retomadas proibidas protegem nodes futuros;
- exemplos repetidos foram removidos;
- referências repetidas têm motivo local.

Se a matriz for genérica demais para orientar `node-pages`, reescreva. Se a
matriz só funcionar dentro de um nível e não impedir repetição entre níveis,
reescreva antes de validar.
