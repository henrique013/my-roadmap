---
name: roadmap-v2-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap-v2` quando a pessoa
  quiser gerar a página inicial de um roadmap pelo pipeline v2.
---

# Roadmap V2 Page

Esta skill é apenas uma flag de seleção para `roadmap-v2`.

Use somente quando a mesma chamada também ativar a skill `roadmap-v2`, por
exemplo:

```text
$roadmap-v2 $roadmap-v2-page
Quero aprender como fazer replicação no Postgres.
```

Se `roadmap-v2` não estiver na mesma chamada, não execute nenhum workflow. Peça
uma nova chamada com `$roadmap-v2 $roadmap-v2-page`.

Se a mesma chamada também ativar `$roadmap-v2-node-page`, não execute nenhum
workflow. Peça que a pessoa escolha somente uma flag de modo.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada deve conter informação suficiente para a skill `roadmap-v2`
identificar:

- o tema do roadmap.

Opcionalmente, a chamada pode mencionar conhecimentos prévios, objetivo,
experiência, senioridade, fontes, limites ou outro contexto relevante. Quando
esse contexto existir, a skill principal deve usá-lo para calibrar a pipeline.

Esta flag define somente seleção de modo e contrato de input. Ela aponta para a
saída visível esperada do modo `roadmap-v2-page`, mas não define processamento,
pesquisa, validação, renderer, scripts nem formato de resposta. Todas as regras
operacionais ficam na skill principal `roadmap-v2`.
