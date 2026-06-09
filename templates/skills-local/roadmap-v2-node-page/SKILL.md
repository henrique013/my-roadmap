---
name: roadmap-v2-node-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap-v2` quando a pessoa
  quiser gerar uma página profunda de node pelo pipeline v2.
---

# Roadmap V2 Node Page

Esta skill é apenas uma flag de seleção para `roadmap-v2`.

Use somente quando a mesma chamada também ativar a skill `roadmap-v2`, por
exemplo:

```text
$roadmap-v2 $roadmap-v2-node-page
replicacao-postgres
basico
01-modelo-mental-da-replicacao
```

Se `roadmap-v2` não estiver na mesma chamada, não execute nenhum workflow. Peça
uma nova chamada com `$roadmap-v2 $roadmap-v2-node-page`.

Se a mesma chamada também ativar `$roadmap-v2-page`, não execute nenhum
workflow. Peça que a pessoa escolha somente uma flag de modo.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada ou o contexto ativo devem conter informação suficiente para a skill
`roadmap-v2` identificar:

- o roadmap v2;
- exatamente um node canônico que deve ter a página gerada.

A chamada pode conter:

- slug do roadmap;
- nível do node;
- `node_id`;
- slug do node.

Texto livre não deve virar caminho de saída diretamente. Um `node_id` com `/`
pode ser usado apenas como identificador lógico para resolução no contrato; ele
não deve ser usado diretamente como caminho.

Esta flag define somente seleção de modo e contrato de input. Todas as regras
operacionais ficam na skill principal `roadmap-v2`.
