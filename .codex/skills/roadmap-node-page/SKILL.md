---
name: roadmap-node-page
description: >
  Flag auxiliar para usar somente junto da skill `roadmap` quando a pessoa
  quiser gerar a página profunda de um node do roadmap.
---

# Roadmap Node Page

Esta skill é apenas uma flag de seleção para `roadmap`.

Use somente quando a mesma chamada também ativar a skill `roadmap`, por exemplo:

```text
/roadmap /roadmap-node-page
replicacao-postgres
01-modelo-mental-da-replicacao
```

Se `roadmap` não estiver na mesma chamada, não execute nenhum workflow. Peça uma
nova chamada com `/roadmap /roadmap-node-page`.

## Input Esperado

A pessoa pode escrever em texto livre. Não exija formato rígido, ordem fixa,
marcadores ou campos nomeados.

A chamada deve conter informação suficiente para a skill `roadmap` identificar:

- o node que deve ter a página gerada.

A chamada pode conter informação para a skill `roadmap` identificar:

- o slug do roadmap.

Exemplos válidos de input incluem slug, título do node, descrição natural,
parágrafo, lista solta ou linhas separadas. Se a identificação do roadmap ou do
node não for suficiente, a skill principal `roadmap` deve pedir somente o dado
necessário.

Esta flag não define processamento, pesquisa, validação, arquivos de saída,
templates, scripts nem formato de resposta. Todas as regras operacionais ficam
na skill principal `roadmap`.
