---
name: roadmap-node-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap` quando a pessoa
  quiser gerar a página profunda de um node do roadmap, resolvido por
  `node_id`, por `level + node-slug` ou por exatamente um candidato canônico do
  contrato do roadmap.
---

# Roadmap Node Page

Esta skill é apenas uma flag de seleção para `roadmap`.

Use somente quando a mesma chamada também ativar a skill `roadmap`, por exemplo:

```text
$roadmap $roadmap-node-page
replicacao-postgres
basico
01-modelo-mental-da-replicacao
```

Se `roadmap` não estiver na mesma chamada, não execute nenhum workflow. Peça uma
nova chamada com `$roadmap $roadmap-node-page`.

Se a mesma chamada também ativar `$roadmap-page`, não execute nenhum workflow.
Peça que a pessoa escolha somente uma flag de modo.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada ou o contexto ativo devem conter informação suficiente para a skill
`roadmap` identificar:

- o roadmap;
- exatamente um node canônico que deve ter a página gerada.

A chamada pode conter informação para a skill `roadmap` identificar:

- o slug do roadmap.
- o nível do node: `basico`, `intermediario` ou `avancado`.
- o `node_id` no formato `<level>/<node-slug>`.
- o slug do node no formato `NN-slug`.

Exemplos válidos de input incluem slug, título do node, descrição natural,
parágrafo, lista solta ou linhas separadas. Em roadmaps tri-level, a skill
principal `roadmap` deve resolver o node por `node_id`, por
`level + node-slug` ou por exatamente um candidato canônico do contrato em
`.roadmap/roadmap-contract.json`. Se o slug aparecer em apenas um nível, o
nível pode ser inferido; se houver ambiguidade de roadmap, nível ou node, a
skill principal deve pedir somente o dado que faltar antes de criar, recriar ou
atualizar arquivos.

Texto livre não deve virar caminho de saída diretamente. Um `node_id` no formato
`<level>/<node-slug>` pode ser usado apenas como identificador para resolução no
contrato; ele não deve ser usado diretamente como caminho. Para o `node-slug`
final, rejeite valores com `/`, `..`, vazios ou fora do contrato canônico.

Esta flag seleciona o modo interno `node-pages` e define somente seleção de
modo e contrato de input. Ela não define processamento, pesquisa, validação,
arquivos de saída, templates, scripts nem formato de resposta. Todas as regras
operacionais ficam na skill principal `roadmap`.
