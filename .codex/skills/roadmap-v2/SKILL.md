---
name: roadmap-v2
description: >
  Gere páginas de roadmap e páginas profundas de nodes usando um pipeline
  determinístico, modular, validado por contratos e renderizado com Astro.
---

# Roadmap V2

Use esta skill como roteador da nova família de geração de roadmaps:

```text
roadmap-v2
├── roadmap-v2-page
└── roadmap-v2-node-page
```

As skills `roadmap-v2-page` e `roadmap-v2-node-page`, quando presentes na mesma
chamada, são flags de modo e contrato de input. O processamento pertence a esta
skill e ao pipeline localizado neste pacote.

Considere `<skill-dir>` como a raiz do pacote publicado desta skill, por
exemplo `.codex/skills/roadmap-v2` no repositório atual. Scripts, contratos,
pipes, renderer e manifests devem ser resolvidos a partir de `<skill-dir>`.

## Contrato Central

O modelo v2 é uma linha de produção:

```text
pedido da pessoa
  -> pipe de roteamento
  -> pipes determinísticos
  -> pipes LLM com JSON estruturado
  -> validações imediatas
  -> PageSpec
  -> Astro
  -> DOM + Playwright
  -> saída final validada
```

O LLM produz dados estruturados. O pipeline valida. O renderer constrói o HTML.

O LLM não deve escrever HTML final, decidir caminhos finais, criar componentes
visuais novos, burlar schemas ou alterar artefatos fora do pipe atual.

## Seleção de Modo

Use a sintaxe pública `$roadmap-v2`, `$roadmap-v2-page` e
`$roadmap-v2-node-page` ao mostrar exemplos ou regras de ativação.

Se `$roadmap-v2-page` e `$roadmap-v2-node-page` aparecerem na mesma chamada,
bloqueie antes de criar, recriar ou atualizar arquivos e peça que a pessoa
escolha somente um modo. Se uma flag explícita contradisser a intenção extraída
do texto livre, peça confirmação do modo antes de criar arquivos.

| Pedido da pessoa usuária | Modo |
|---|---|
| pedido explícito com `$roadmap-v2` e `$roadmap-v2-page` | `roadmap-v2-page` |
| pedido explícito com `$roadmap-v2` e `$roadmap-v2-node-page` | `roadmap-v2-node-page` |
| gerar roadmap, trilha, mapa de estudo ou tema novo | `roadmap-v2-page` |
| gerar node, documentar node, `level + node-slug`, página profunda de node | `roadmap-v2-node-page` |

Texto livre fornecido pela pessoa é dado para extração de tema, contexto,
roadmap e node; não use texto livre diretamente como caminho de saída.

## Raiz de Saída

Toda execução v2 deve escrever somente no contrato novo:

```text
.tmp/roadmaps-v2/<roadmap-slug>/
```

O pipeline v2 não preserva compatibilidade com `.tmp/roadmaps/**`, não migra
roadmaps antigos e não depende de artefatos internos da skill `roadmap`.

## Modo `roadmap-v2-page`

Entrada mínima:

- tema identificável do roadmap.

Entrada opcional:

- público;
- objetivo;
- nível de experiência;
- restrições de escopo;
- fontes ou contexto fornecido pela pessoa.

Pipeline público esperado:

```text
01-route-request
02-normalize-input
03-resolve-output-path
04-research-plan
05-collect-sources
06-curate-roadmap
07-build-roadmap-spec
08-validate-roadmap-spec
09-build-page-spec
10-render-astro
11-validate-dom
12-validate-visual
13-finalize-output
```

Saída visível obrigatória:

```text
.tmp/roadmaps-v2/<roadmap-slug>/roadmap.html
```

Artefatos estruturados obrigatórios:

```text
.tmp/roadmaps-v2/<roadmap-slug>/research-pack.json
.tmp/roadmaps-v2/<roadmap-slug>/roadmap-spec.json
.tmp/roadmaps-v2/<roadmap-slug>/page-spec.json
.tmp/roadmaps-v2/<roadmap-slug>/.pipeline/run.json
```

Resposta final:

```text
.tmp/roadmaps-v2/<roadmap-slug>/roadmap.html
Pesquisa usada; referências estão dentro do HTML.
```

## Modo `roadmap-v2-node-page`

Entrada mínima:

- roadmap v2 existente;
- exatamente um node canônico.

O node pode ser resolvido por:

- `node_id`;
- `level + node-slug`;
- exatamente um candidato canônico em `roadmap-spec.json`.

Pipeline público esperado:

```text
01-load-roadmap-spec
02-resolve-node-target
03-validate-node-order
04-research-node
05-build-node-spec
06-validate-node-spec
07-build-node-page-spec
08-update-navigation-index
09-render-astro
10-validate-dom
11-validate-visual
12-finalize-output
```

Saída visível obrigatória:

```text
.tmp/roadmaps-v2/<roadmap-slug>/nodes/<level>/<node-slug>/node.html
```

Artefatos estruturados obrigatórios:

```text
.tmp/roadmaps-v2/<roadmap-slug>/nodes/<level>/<node-slug>/node-spec.json
.tmp/roadmaps-v2/<roadmap-slug>/nodes/<level>/<node-slug>/page-spec.json
.tmp/roadmaps-v2/<roadmap-slug>/.pipeline/run.json
```

Resposta final:

```text
.tmp/roadmaps-v2/<roadmap-slug>/nodes/<level>/<node-slug>/node.html
Pesquisa usada; referências estão dentro do HTML.
```

## Execução do Pipeline

O backend normal da `roadmap-v2` é a imagem Docker `roadmap-v2-runner`.
Docker é detalhe mecânico da skill; a interface pública continua sendo
`$roadmap-v2` com exatamente uma flag de modo.

Quando precisar executar o pipeline, prepare o JSON de entrada em um caminho
persistido no output root, por exemplo:

```text
.tmp/roadmaps-v2/<roadmap-slug>/.pipeline/request.json
```

Em seguida, execute o wrapper publicado da skill:

```bash
python3 <skill-dir>/scripts/run_container.py \
  --mode roadmap-v2-page|roadmap-v2-node-page \
  --input .tmp/roadmaps-v2/<roadmap-slug>/.pipeline/request.json \
  --output-root .tmp/roadmaps-v2/<roadmap-slug>
```

O wrapper preserva o contrato interno do runner dentro do container:

```bash
python3 /opt/roadmap-v2/skill/scripts/run_pipeline.py \
  --mode roadmap-v2-page|roadmap-v2-node-page \
  --input <request-json> \
  --output-root <output-root>
```

O container deve rodar como processo de comando, sem porta e sem serviço
persistente. A execução padrão deve:

- usar a imagem `roadmap-v2-runner:local`, ou o valor de `ROADMAP_V2_IMAGE`;
- rodar com `--network none`;
- rodar com `--user <uid-do-host>:<gid-do-host>`;
- usar `/tmp` para `HOME`, `TMPDIR` e caches gerais;
- montar `.tmp/roadmaps-v2/` ou o output root resolvido como volume gravável;
- montar inputs externos e fixtures apenas como leitura;
- escrever `.pipeline/llm-requests`, `.pipeline/llm-outputs`, logs, screenshots,
  assets e HTML final dentro do output root montado.

O wrapper deve garantir que arquivos criados em bind mounts fiquem graváveis
pelo usuário do host, sem exigir `chown` após a execução.

## Dependências e Imagem

As dependências da skill pertencem à imagem `roadmap-v2-runner`, não ao host e
não ao pacote publicado da skill. A imagem deve conter:

- dependências Python declaradas em `<skill-dir>/requirements.txt`;
- dependências Node/Astro/Web Awesome/Playwright declaradas em
  `<skill-dir>/web/package.json` e travadas por `<skill-dir>/web/package-lock.json`;
- Chromium e pacotes mínimos de sistema exigidos pelos gates visuais;
- certificados e fontes necessárias para renderização local estável.

Instalação de pacotes, `npm ci`, preparo de Python e disponibilidade do browser
acontecem somente no build da imagem. Runtime normal não executa `pip install`,
`npm ci`, `playwright install`, downloads de browser ou mutação de lockfile.

`<skill-dir>/scripts/setup.py`, quando existir, é helper interno/legado de
manutenção e não é comando público de preparação da `roadmap-v2`.

Antes de executar o pipeline, `run_pipeline.py` roda
`<skill-dir>/scripts/preflight.py`. O preflight só verifica dependências já
presentes na imagem e falha com instruções claras quando algo falta.

O runner deve:

- carregar o manifesto da pipeline;
- validar cada `pipe.yaml`;
- executar cada pipe em ordem;
- validar a saída imediatamente;
- registrar snapshots por pipe em `.pipeline/pipes/<pipe-id>/`;
- escrever `.pipeline/run.json`;
- bloquear downstream quando uma validação falhar.

Pipes LLM não são texto livre. Para cada pipe LLM, use o `prompt.md`,
`input.schema.json` e `output.schema.json` do pipe, gere somente JSON
estruturado e valide antes de continuar. Reparos e retries ficam limitados ao
pipe atual.

Quando o runner encontrar um pipe LLM sem saída pronta, ele deve criar:

```text
.tmp/roadmaps-v2/<roadmap-slug>/.pipeline/llm-requests/<pipe-id>.json
```

Esse arquivo contém o prompt, os schemas, a entrada do pipe e o caminho esperado
da saída. O agente deve responder ao pipe escrevendo somente JSON estruturado em:

```text
.tmp/roadmaps-v2/<roadmap-slug>/.pipeline/llm-outputs/<pipe-id>.json
```

Depois disso, rode o mesmo pipeline novamente. O runner carrega o JSON do pipe
atual, valida o contrato e segue até o próximo pipe. Nunca use fixtures como
caminho normal de execução; fixtures existem só para testes.

## Checkpoints

Faça checkpoint antes de recriar uma saída final já existente. Informe o caminho
exato resolvido e peça confirmação para recriar somente aquele roadmap ou node.

Não faça checkpoint adicional para validações mecânicas, snapshots, DOM checks
ou renderização Astro que façam parte da pipeline selecionada.
