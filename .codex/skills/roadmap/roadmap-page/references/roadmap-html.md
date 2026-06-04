# Contrato de `roadmap.html`

`roadmap.html` é a página humana do roadmap. Ela deve ser autocontida, legível e
coerente com `.roadmap/roadmap-contract.json`.

## Estrutura Obrigatória

O HTML deve conter:

- `<!doctype html>`;
- `html lang="pt-BR"`;
- `meta charset="utf-8"`;
- viewport;
- CSS embutido;
- `<title>` e `<h1>`;
- contexto informado ou premissa neutra;
- compreensão final esperada;
- data da pesquisa;
- premissas e limites;
- mapa da corrente;
- lista resumida dos nodes;
- matriz anti-repetição;
- seções completas dos nodes;
- checklist final de cobertura;
- referências consolidadas.

## Seções de Node

Cada seção de node deve expor:

- label;
- slug `NN-slug`;
- papel na corrente;
- pré-requisitos herdados;
- o que introduz pela primeira vez;
- o que deve cobrir;
- o que não deve cobrir;
- perguntas;
- vocabulário conceitual;
- exemplos conceituais ou diagramas permitidos;
- armadilhas;
- critério de domínio;
- handoff;
- referências específicas.

O HTML deve ajudar outro agente a gerar `node-pages` sem adivinhar escopo.

## Proibições

- Não deixe Markdown cru.
- Não crie `prompt.md`.
- Não gere laboratório, exercício, hands-on, desafio prático ou projeto final.
- Não transforme comandos em roteiro de execução.
- Não use texto de corpo com largura menor que a largura útil sem justificativa
  visual explícita.
- Não use `<pre>` como atalho para mapa, fluxo, sequência, linha do tempo,
  estado ou contraste conceitual simples.

## Primitivas Visuais

Use tabelas para matrizes, listas e referências. Use componentes HTML/CSS para
mapas, fluxos, sequências e relações visuais. Use `<pre>` apenas para texto
literal, código, configuração ou ASCII excepcional justificado.

Quando ASCII for exceção, o bloco deve ter `data-ascii-exception="true"`,
`data-ascii-reason` não vazio e justificativa no audit visual.

## Relação com o Contrato JSON

O HTML e o JSON devem concordar sobre:

- slug do roadmap;
- ordem dos nodes;
- slug e label de cada node;
- conceitos introduzidos;
- escopo positivo e negativo;
- referências por node;
- matriz anti-repetição.

Se houver divergência, corrija o HTML ou o JSON antes de responder.
