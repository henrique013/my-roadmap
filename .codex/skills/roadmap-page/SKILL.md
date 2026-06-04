---
name: roadmap-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap` quando a pessoa
  quiser gerar a página inicial tri-level de um roadmap.
---

# Roadmap Page

Esta skill é apenas uma flag de seleção para `roadmap`.

Use somente quando a mesma chamada também ativar a skill `roadmap`, por exemplo:

```text
/roadmap /roadmap-page
Quero aprender como fazer replicação no Postgres.
```

Se `roadmap` não estiver na mesma chamada, não execute nenhum workflow. Peça uma
nova chamada com `/roadmap /roadmap-page`.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada deve conter informação suficiente para a skill `roadmap` identificar:

- o tema do roadmap.

Opcionalmente, a chamada pode mencionar conhecimentos prévios, objetivo,
experiência, senioridade ou outro contexto relevante. Quando esse contexto
existir, a skill principal `roadmap` deve usá-lo para calibrar o resultado, sem
tratá-lo como campo esperado ou requisito.

Quando esta flag seleciona `roadmap-page`, a skill principal `roadmap` gera uma
única saída visível em `.tmp/roadmaps/<slug>/roadmap.html` com três seções
coordenadas:

- `basico`;
- `intermediario`;
- `avancado`.

Cada nível pode ter até 20 nodes, mas esse número é teto, não meta. A skill
principal deve planejar os três níveis no mesmo contexto para reduzir
sobreposição e manter a anti-repetição global.

Exemplos válidos de input incluem frase curta, parágrafo, lista solta ou linhas
separadas. Se o tema não for identificável no texto livre, a skill principal
`roadmap` deve pedir somente o tema.

Esta flag não define processamento, pesquisa, validação, arquivos de saída,
templates, scripts nem formato de resposta. Todas as regras operacionais ficam
na skill principal `roadmap`.
