# Auditoria de escolha de primitiva visual

## Status

Status geral: passa

## Primitivas avaliadas

| Relação | Primitiva usada | Motivo | Status |
|---|---|---|---|
| Exchange sem bindings versus com bindings | Componente HTML/CSS de estado antes/depois | Mostra estado e diferença com fila vazia sem usar diagrama ASCII | passa |
| Routing key versus binding key | Snippet conceitual com highlight e tabela | A forma literal dos campos é necessária para separar publicação e regra | passa |
| Uma publicação alcançando múltiplos destinos | Mapa HTML/CSS de source, bindings e destinations | Topologia e cardinalidade ficam mais claras como mapa | passa |
| Destination type | Tabela curta | Classificação de campos é melhor como tabela do que prosa corrida | passa |
| Leitura de topologia pequena | Cards numerados em HTML/CSS | Sequência conceitual curta, sem comandos | passa |

## Checks de ASCII e pre

- Nenhum visual conceitual simples usa `<pre>`.
- O único `<pre><code>` é snippet conceitual de campos, não diagrama.
- Não há exceção ASCII.
- O snippet tem highlight semântico por classes `syntax-*`.

## Conclusão

Status: passa. As primitivas visuais foram escolhidas pelo tipo de entendimento necessário e não por decoração.
