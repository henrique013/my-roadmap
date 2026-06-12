# Example sufficiency audit

Status geral: passa

## Exemplos e suportes concretos

| Suporte | Demanda didática | Resultado |
|---|---|---|
| Exemplo `orders-api` / `orders.events` / `orders.created` | Conduzir a explicação sem laboratório | passa |
| Topologia publisher -> exchange -> filas | Mostrar fronteira de conhecimento entre producer, topologia e consumidores | passa |
| Tabela `orders.created` versus `billing.orders-created` | Separar intenção de publicação de detalhe de fila | passa |
| Antes/depois com fila de auditoria | Mostrar mudança de topologia sem alterar publisher | passa |
| Matriz domínio/evento/severidade/tenant | Comparar recortes exigidos pelo contrato | passa |
| Cards de relação material | Mostrar exchange pública, filas internas e bindings sem configuração | passa |

## Suficiência qualitativa

- O exemplo condutor retorna em mais de um bloco: abertura, visual de topologia, tabela, antes/depois e cards de relação.
- Não há snippet técnico; a página evita comandos e usa visual HTML/CSS para relações conceituais.
- A página não vira laboratório: não há setup, client library, comando de importação, endpoint ou roteiro de execução.
- O próximo node é apenas preparado no fechamento; não há explicação de broadcast versus competição.

## Decisão

Os exemplos concretizam forma, estado, contraste e fronteira sem excesso. O HTML não precisa de reescrita.
