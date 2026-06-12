# Concept introduction audit

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

- Conceitos do node podem aparecer no título e no contexto de posição por contrato do roadmap.
- No corpo narrativo, a página prepara a necessidade antes de depender de cada termo técnico.
- Termos bloqueados literais foram verificados com `scan_blocked_terms.py`.
- Conceitos reservados a nodes futuros não sustentam a explicação do node atual.

## Primeiras ocorrências auditadas

| Conceito | Primeira ocorrência relevante | Preparação observada | Status |
|---|---|---|---|
| Tipo de exchange como regra de decisão | Lead | O texto parte de bindings já conhecidos e pergunta como a exchange avalia a routing key. | passa |
| Direct exchange | Título e contexto por contrato; corpo em "Direct resolve quando a etiqueta precisa bater" | Antes da nomeação no corpo, a página explica igualdade entre routing key e binding key. | passa |
| Fanout exchange | Título e contexto por contrato; corpo em "Fanout resolve quando escolher não faz parte da intenção" | Antes da nomeação no corpo, a página explica cópia para todos os destinos ligados. | passa |
| Topic exchange | Título e contexto por contrato; corpo em "Topic entra quando a key vira uma frase curta" | Antes da nomeação no corpo, a página explica key com segmentos separados por ponto. | passa |
| Wildcard `*` | Seção topic, após explicação de segmentos | O HTML explica segmento antes de apresentar `audit.*.login`. | passa |
| Wildcard `#` | Seção topic, após `*` | O HTML explica que a cerquilha cobre zero ou mais segmentos e só depois fala do risco. | passa |
| Broadcast | Tabela e callout de fanout | A cópia para todos os destinos ligados aparece antes do termo. | passa |
| Multicast em direct | Card de consequência em direct | O HTML mostra duas filas com a mesma key antes de nomear a consequência. | passa |
| Binding key e routing key | Lead | Pré-requisito herdado do node 03; não há redefinição extensa. | passa |

## Vazamentos encontrados

Nenhum vazamento literal de termo bloqueado foi encontrado. A menção ao próximo node no contexto de posição é obrigatória pela navegação do roadmap e não sustenta a explicação.

## Termos de fonte e referência

| Fonte visível | Termos carregados | Status |
|---|---|---|
| RabbitMQ - Exchanges | exchange | passa; termo já é base do roadmap |
| RabbitMQ - Modelo AMQP 0-9-1 | AMQP | passa; base já apresentada no roadmap e nodes anteriores |
| Tutorial oficial de publish/subscribe | publish/subscribe | passa; aparece após fanout e não abre laboratório |
| Tutorial oficial de roteamento | roteamento | passa; termo herdado |
| Tutorial oficial de tópicos | tópicos | passa; aparece após topic |
| Especificação AMQP 0-9 | AMQP | passa; referência factual |

## Conceitos reservados a nodes futuros

- Headers/metadados aparecem somente como label real do próximo node no contexto de posição.
- Não há uso visível de DLX, AE, mandatory, policies, plugins, E2E ou consumers competindo.

## Resultado da rodada

- HTML precisa reescrita: não

