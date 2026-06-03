---
name: roadmap-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap` quando a pessoa
  quiser gerar a página inicial de um roadmap.
---

# Roadmap Page

Esta skill é apenas uma flag de seleção para `roadmap`.

Use somente quando a mesma chamada também ativar a skill `roadmap`, por exemplo:

```text
/roadmap /roadmap-page
Quero aprender como fazer replicação no Postgres.
Tenho conhecimento intermediário em SQL.
```

Se `roadmap` não estiver na mesma chamada, não execute nenhum workflow. Peça uma
nova chamada com `/roadmap /roadmap-page`.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada deve conter informação suficiente para a skill `roadmap` identificar:

- o tema do roadmap.

A chamada pode conter informação para a skill `roadmap` identificar:

- o background de conhecimento dela.

Exemplos válidos de input incluem frase curta, parágrafo, lista solta ou linhas
separadas. Se o tema não for identificável no texto livre, a skill principal
`roadmap` deve pedir somente o tema.

Esta flag não define processamento, pesquisa, validação, arquivos de saída,
templates, scripts nem formato de resposta. Todas as regras operacionais ficam
na skill principal `roadmap`.
