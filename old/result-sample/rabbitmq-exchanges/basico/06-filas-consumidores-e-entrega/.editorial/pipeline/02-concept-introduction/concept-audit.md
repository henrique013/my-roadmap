# Concept introduction audit

## Status geral

Status geral: passa

## Evidência

- `visible-text.md` foi extraído do `node.html` final da rodada.
- A varredura literal de termos bloqueados contra o ledger passou sem ocorrências.
- O HTML apresenta primeiro a situação de uma mensagem já roteada para a fila `emails`; só depois estabiliza fila, mensagem pronta, delivery, consumer, inscrição e acknowledgement.
- `acknowledgement` aparece depois da distinção entre entrega e remoção segura.
- O contraste entre consumers competindo e cópias por fila aparece depois de consumer e fila já estarem preparados.
- Termos reservados a nodes futuros não sustentam a explicação visível.

## Primeiras ocorrências relevantes

| Conceito | Primeira ocorrência visível | Status |
|---|---|---|
| Fila | Título e lead, como conceito herdado do nível básico | passa |
| Mensagem pronta | Seção sobre estados da fila, depois de a fila ser definida como acúmulo | passa |
| Delivery | Seção sobre estados, após o envio para worker ser explicado | passa |
| Consumer | Lead e narrativa inicial, como aplicação que recebe da fila | passa |
| Subscription | Texto "se registra na fila", antes do termo técnico ficar necessário | passa |
| Acknowledgement | Após a diferença entre entrega e remoção segura | passa |
| Consumers competindo | Depois da fila com três workers | passa |
| Cópia por fila | Depois do visual de várias filas independentes | passa |

## Resultado

Nenhuma reescrita obrigatória foi identificada neste guardrail.
