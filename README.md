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

A família atual de geração é a `roadmap`:

| Skill | O que faz |
|---|---|
| `roadmap` | Skill principal. Roteia a geração da página inicial e das páginas profundas. |
| `roadmap-page` | Flag usada quando você quer criar a página inicial tri-level de um roadmap. |
| `roadmap-node-page` | Flag usada quando você quer criar a página profunda de um node do roadmap. |

Na prática, você sempre usa `roadmap` junto com uma das flags.

## Runtime

A família `roadmap` não exige preparação de runtime no repositório.

Depois de clonar o repositório, o comando abaixo existe apenas como ponto de entrada padrão:

```bash
make setup
```

Ele não instala dependências nem prepara Docker. As validações visuais usam as dependências Node já declaradas no projeto quando forem executadas.

## Como gerar um roadmap

Use a skill principal com a flag de página inicial:

```text
$roadmap $roadmap-page
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
.tmp/roadmaps/<slug-do-roadmap>/roadmap.html
```

Exemplo:

```text
.tmp/roadmaps/replicacao-postgres/roadmap.html
```

Abra esse arquivo no navegador para ver o roadmap final.

## Como gerar a página de um node

Depois que o roadmap inicial existir, você pode pedir uma página profunda para um node específico:

```text
$roadmap $roadmap-node-page
replicacao-postgres
basico
01-modelo-mental-da-replicacao
```

Você também pode identificar o node pelo `node_id`, pelo nível com slug, ou pelo título quando houver exatamente um candidato canônico no contrato do roadmap.

Ao final, o projeto gera:

```text
.tmp/roadmaps/<slug-do-roadmap>/<level>/<slug-do-node>/node.html
```

Exemplo:

```text
.tmp/roadmaps/replicacao-postgres/basico/01-modelo-mental-da-replicacao/node.html
```

Abra esse arquivo no navegador para estudar o node em detalhe.

## Onde ficam os resultados

Os resultados visíveis ficam em `.tmp/roadmaps/`.

Estrutura típica:

```text
.tmp/roadmaps/
└── replicacao-postgres/
    ├── roadmap.html
    ├── .roadmap/
    │   └── roadmap-contract.json
    └── basico/
        └── 01-modelo-mental-da-replicacao/
            ├── research-dump.md
            └── node.html
```

A pasta `.tmp/` é uma área local de saída gerada. Ela serve para você abrir, revisar e usar os roadmaps produzidos.

## Fluxo recomendado

1. Gere primeiro a página inicial do roadmap com `$roadmap` + `$roadmap-page`.
2. Abra o `roadmap.html` no navegador.
3. Escolha o primeiro node que quer estudar em profundidade.
4. Gere a página desse node com `$roadmap` + `$roadmap-node-page`.
5. Repita o processo para os próximos nodes conforme avançar.

## Observação

Este projeto não tenta substituir estudo, prática ou experiência real. Ele organiza o caminho: mostra os pré-requisitos, a sequência de aprendizado e os pontos que precisam ser entendidos para chegar ao conhecimento alvo.
