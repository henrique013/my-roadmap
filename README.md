# My Roadmap

`my-roadmap` existe para criar roadmaps de aprendizado customizados.

A ideia é simples: a pessoa escolhe uma habilidade, um conhecimento ou um tema que quer aprender, informa o ponto de partida quando isso for útil, e o projeto gera uma trilha sequencial com os conhecimentos prévios necessários até chegar no nível desejado.

Em vez de entregar uma lista genérica de tópicos, o roadmap desenha uma árvore de dependências: o que vem antes, o que depende de quê e qual caminho faz sentido seguir para dominar o assunto alvo.

## Para que serve

Use este projeto quando quiser transformar um objetivo de aprendizado em uma trilha navegável.

Exemplos de temas:

- aprender replicação no Postgres;
- entender fundamentos de sistemas distribuídos;
- estudar React do zero até um nível profissional;
- aprender machine learning com base matemática limitada;
- dominar um conceito específico dentro de uma área maior.

O resultado principal é uma página HTML do roadmap, com os nodes organizados em sequência. Depois, cada node pode ganhar uma página própria, mais profunda, para explicar aquele conhecimento específico.

## Como o projeto é organizado

A família atual de geração é a `roadmap-v2`:

| Skill | O que faz |
|---|---|
| `roadmap-v2` | Skill principal. Roteia e executa o pipeline determinístico. |
| `roadmap-v2-page` | Flag usada quando você quer criar a página inicial de um roadmap. |
| `roadmap-v2-node-page` | Flag usada quando você quer criar a página profunda de um node do roadmap. |

Na prática, você sempre usa `roadmap-v2` junto com uma das flags.

## Runtime

A `roadmap-v2` roda por uma imagem Docker local, sem preparar Python, Node,
Astro, Web Awesome, Playwright ou Chromium no workspace.

Depois de clonar o repositório, rode:

```bash
make setup
```

Esse comando constrói a imagem `roadmap-v2-runner:local` e remove somente os
runtimes legados gerados da `roadmap-v2`.

Para usar outro nome/tag de imagem, defina `ROADMAP_V2_IMAGE`.

O runtime antigo gerado em `.codex-runtime/roadmap-v2/` ou
`.codex/runtime/roadmap-v2/` não faz parte do fluxo normal. O `make setup`
remove somente esses diretórios de runtime legado; ele não remove roadmaps
gerados em `.tmp/roadmaps-v2/`.

## Como gerar um roadmap

Use a skill principal com a flag de página inicial:

```text
$roadmap-v2 $roadmap-v2-page
Quero aprender replicação no Postgres.
Tenho conhecimento intermediário em SQL e já usei Postgres em aplicações simples.
Quero chegar a um nível em que eu consiga entender, operar e diagnosticar replicação em produção.
```

Você pode escrever em texto livre. O importante é deixar claro:

- qual tema quer aprender;
- qual é seu ponto de partida, se quiser personalizar melhor;
- qual nível de domínio você quer alcançar.

Ao final, o projeto gera uma página em:

```text
.tmp/roadmaps-v2/<slug-do-roadmap>/roadmap.html
```

Exemplo:

```text
.tmp/roadmaps-v2/replicacao-postgres/roadmap.html
```

Abra esse arquivo no navegador para ver o roadmap final.

## Como gerar a página de um node

Depois que o roadmap inicial existir, você pode pedir uma página profunda para um node específico:

```text
$roadmap-v2 $roadmap-v2-node-page
replicacao-postgres
01-modelo-mental-da-replicacao
```

Você também pode identificar o node pelo título, desde que fique claro qual node deve ser aprofundado.

Ao final, o projeto gera:

```text
.tmp/roadmaps-v2/<slug-do-roadmap>/nodes/<level>/<slug-do-node>/node.html
```

Exemplo:

```text
.tmp/roadmaps-v2/replicacao-postgres/nodes/basico/01-modelo-mental-da-replicacao/node.html
```

Abra esse arquivo no navegador para estudar o node em detalhe.

## Onde ficam os resultados

Os resultados visíveis da v2 ficam em `.tmp/roadmaps-v2/`.

Estrutura típica:

```text
.tmp/roadmaps-v2/
└── replicacao-postgres/
    ├── roadmap.html
    ├── roadmap-spec.json
    ├── page-spec.json
    └── nodes/
        └── basico/
            └── 01-modelo-mental-da-replicacao/
                └── node.html
```

A pasta `.tmp/` é uma área local de saída gerada. Ela serve para você abrir, revisar e usar os roadmaps produzidos.

## Fluxo recomendado

1. Gere primeiro a página inicial do roadmap com `$roadmap-v2` + `$roadmap-v2-page`.
2. Abra o `roadmap.html` no navegador.
3. Escolha o primeiro node que quer estudar em profundidade.
4. Gere a página desse node com `$roadmap-v2` + `$roadmap-v2-node-page`.
5. Repita o processo para os próximos nodes conforme avançar.

## Observação

Este projeto não tenta substituir estudo, prática ou experiência real. Ele organiza o caminho: mostra os pré-requisitos, a sequência de aprendizado e os pontos que precisam ser entendidos para chegar ao conhecimento alvo.
