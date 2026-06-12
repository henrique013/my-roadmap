# Concept introduction audit

## Metadados

- Roadmap: `rabbitmq-exchanges`
- Level: `basico`
- Node: `01-modelo-amqp-e-papel-da-exchange`
- HTML auditado: `node.html`
- Texto extraído: `.editorial/pipeline/01-visible-text/visible-text.md`
- Ledger: `.editorial/concept-ledger.md`
- Data: 2026-06-08

## Status geral

Status geral: passa

## Checks

| Check | Status | Evidência |
|---|---|---|
| conceitos centrais são preparados antes do uso forte | passa | O HTML abre com a necessidade de publicar sem acoplar produtor a consumers antes de nomear exchange como ponto de roteamento. |
| exchange, fila e consumer têm fronteiras claras | passa | O texto e o mapa de responsabilidades separam roteamento, armazenamento e processamento. |
| binding aparece só como ligação suficiente para o node 01 | passa | O HTML usa binding como ligação configurada, sem entrar em chaves ou argumentos. |
| conceitos reservados a nodes futuros não sustentam a explicação | passa | A única menção ao próximo node aparece no contexto/handoff; não há explicação de exchange padrão. |
| busca literal de termos bloqueados | passa | `scan_blocked_terms.py` retornou "passa: nenhum termo bloqueado literal encontrado". |
| referências não introduzem conceito técnico sem preparo | passa | Títulos visíveis das fontes usam termos permitidos no ledger. |

## Primeiras ocorrências auditadas

| Conceito | Primeira ocorrência relevante | Status |
|---|---|---|
| AMQP 0-9-1 | lead, após apresentar publicação no RabbitMQ | passa |
| exchange | lead, já associada a ponto de entrada e decisão de filas | passa |
| publisher / producer | seção de caminho, depois da aplicação publicadora | passa |
| broker | primeira seção, como serviço intermediário | passa |
| binding | seção de caminho, depois de exchange e fila | passa |
| fila / queue | lead e primeira seção, como destino que recebe mensagens | passa |
| consumer | lead e fluxo, como aplicação que recebe a partir da fila | passa |
| cópia da mensagem | fluxo e resultados possíveis, depois de múltiplas filas | passa |

## Decisão

Nenhuma reescrita é obrigatória.
