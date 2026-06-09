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

O runner Python fica em:

```text
<skill-dir>/scripts/run_pipeline.py
```

Execute o runner pelo script publicado da skill:

```bash
python3 <skill-dir>/scripts/run_pipeline.py
```

Depois do setup, o runner reexecuta automaticamente com o Python isolado da
skill quando esse runtime existir.

## Dependências e Setup

As dependências da skill devem ser preparadas pelo setup público da própria
skill, não durante a execução do pipeline:

```bash
python3 <skill-dir>/scripts/setup.py
```

Esse setup instala:

- dependências Python declaradas em `<skill-dir>/requirements.txt`;
- dependências Node/Astro/Web Awesome/Playwright declaradas em
  `<skill-dir>/web/package.json` e travadas por `<skill-dir>/web/package-lock.json`;
- browser Chromium usado pelos gates visuais do Playwright.

Por padrão, os arquivos gerados pelo setup ficam fora do pacote da skill:

```text
.codex/runtime/roadmap-v2/
├── python/
├── node/
├── browsers/
└── cache/
```

Quando `.codex` estiver montado como read-only, o default efetivo é:

```text
.codex-runtime/roadmap-v2/
├── python/
├── node/
├── browsers/
└── cache/
```

O caminho pode ser alterado com `ROADMAP_V2_RUNTIME_HOME`. Se o repositório
consumidor oferecer `make setup` ou scripts npm, trate-os apenas como atalhos
para o setup público da skill.

Antes de executar o pipeline, `run_pipeline.py` roda
`<skill-dir>/scripts/preflight.py`. O preflight só verifica dependências e
falha com instruções claras quando algo falta; ele não instala pacotes, não
altera lockfiles e não baixa browser em runtime.

O único comando público de preparação do ambiente é:

```bash
python3 <skill-dir>/scripts/setup.py
```

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
