# Concept introduction audit

Status: passa

## Escopo auditado

- HTML: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/05-policies-x-arguments-e-permissoes/node.html`
- Ledger: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/05-policies-x-arguments-e-permissoes/.editorial/concept-ledger.md`
- Texto visível: `.tmp/roadmaps/rabbitmq-exchanges/intermediario/05-policies-x-arguments-e-permissoes/.editorial/pipeline/01-visible-text/visible-text.md`

## Primeiras ocorrências

| Conceito | Status | Evidência |
|---|---|---|
| Policy | passa | O título carrega o label canônico; no corpo, a necessidade de mudar várias filas sem redeploy aparece antes da definição. |
| X-argument | passa | O corpo explica argumentos opcionais enviados na declaração antes de depender do termo. |
| Runtime parameter | passa | Só aparece depois que policy já foi situada como regra mantida pelo broker. |
| Operator policy | passa | Aparece depois da pergunta sobre conflito de autoridade e é explicada como guardrail. |
| Precedência | passa | O texto primeiro mostra disputa de chave entre camadas e depois nomeia a regra. |
| Vhost | passa | O texto prepara espaço lógico de recursos antes de usar o termo como fronteira. |
| Configure, write e read | passa | A página explica o sentido de cada permissão antes da tabela de operações. |

## Termos bloqueados

O script `scan_blocked_terms.py` passou sem candidatos literais. A leitura semântica também não encontrou vazamento de declaração passiva, backends de autenticação, publisher confirms, diagnóstico operacional ou composição local entre exchanges fora do contexto permitido de navegação.

## Risco de tom corretivo

Status: passa. A narrativa abre com uma situação de mudança de DLX em grupo de filas, constrói o modelo positivo de camadas de autoridade e só depois aponta riscos de rigidez, permissões amplas e escopo de policy.

## Decisão

Não há reescrita obrigatória por introdução conceitual.
