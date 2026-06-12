# Example sufficiency audit

Status: passa

## Exemplos e suportes concretos

| Suporte | Status | Evidência |
|---|---|---|
| Exemplo condutor `orders.*` | passa | O exemplo aparece na abertura, no contraste entre declaração e policy, na discussão de permissões e na matriz de ownership. |
| Snippet conceitual | passa | O bloco mostra forma de configuração, tem aviso de que não é roteiro de execução e não contém comandos. |
| Contraste hardcoded vs policy | passa | O componente HTML/CSS mostra antes, mudança e depois, reduzindo abstração sem repetir o node de DLX. |
| Camadas de autoridade | passa | O visual de três cards mostra declaração, policy comum e operator policy como fontes de valor efetivo. |
| Tabela de permissões | passa | A tabela reduz ambiguidade entre configure, write e read em operações relevantes ao roadmap. |
| Vhost como fronteira lógica | passa | O mapa de dois vhosts mostra nomes iguais em fronteiras diferentes sem prometer isolamento físico. |

## Excesso evitado

- Não há roteiro de execução ou sequência de comandos.
- Não há reensino de AE, DLX, causas de dead-lettering ou retry.
- Não há matriz completa de segurança RabbitMQ.
- Não há lista exaustiva de chaves de policy.

## Decisão

Os exemplos são suficientes para forma, contraste, fronteira e mapeamento. Não há reescrita obrigatória por falta ou excesso de concretização.
