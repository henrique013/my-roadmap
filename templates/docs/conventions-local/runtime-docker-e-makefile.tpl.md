# Runtime Docker Aberto

<!-- AGENT-CARD START -->
Leia este documento ao alterar o runtime Docker, comandos que usam
`docker/runtime/run` ou dependências de execução do projeto.
Use este documento para decidir o que pode rodar no host, o que deve rodar em
imagem Docker e onde declarar comandos específicos de um fluxo.
<!-- AGENT-CARD END -->

Esta convenção define o wrapper `docker/runtime/run` como uma fachada aberta
para a imagem runtime do projeto. O wrapper não é orquestrador de domínio, não
conhece workflows específicos e não substitui as instruções das skills.

## Regra central

- Trate Docker, Node e Python como as únicas dependências esperadas no host
  quando forem exigidas por fluxos já contratados do repositório.
- Não instale ferramentas ad hoc no host para executar validações, gerar
  artefatos, renderizar páginas, baixar navegadores, compilar dependências
  nativas ou completar uma tarefa pontual.
- Coloque dependências adicionais na imagem runtime ou em uma imagem Docker
  específica.
- Declare comandos específicos de cada fluxo na skill, spec ou documento que
  governa esse fluxo.
- Mantenha `docker/runtime/run` aberto: ele recebe um comando arbitrário e o
  executa dentro da imagem runtime.

## Contrato do `docker/runtime/run`

Use `docker/runtime/run` para executar comandos que pertencem ao ambiente
runtime do projeto:

```text
docker/runtime/run <comando> [args...]
```

O wrapper deve:

- montar o repositório inteiro em `/workspace`;
- usar `/workspace` como diretório de trabalho;
- executar com UID/GID do usuário do host;
- configurar `HOME`, caches e `PLAYWRIGHT_BROWSERS_PATH` para o runtime;
- criar `/tmp` efêmero com `tmpfs`;
- usar rede `none` por padrão;
- usar IPC `host` por padrão;
- executar preflight genérico de Docker daemon e imagem configurada antes de
  chamar `docker run`;
- repassar o comando recebido sem interpretar flags de domínio.

O wrapper não deve:

- validar variáveis de fluxos específicos, como `ROADMAP_DIR`, `LEVEL` ou
  `NODE`;
- ter catálogo de targets;
- ter modo de build;
- expor modo de preflight separado como substituto do comando runtime normal;
- construir imagem automaticamente;
- esconder comandos de validação que pertencem às skills.

## Configuração suportada

| Aspecto | Comportamento |
|---|---|
| Imagem padrão | `my-roadmap-roadmap-runtime:playwright-1.60.0` |
| Diretório no contêiner | `/workspace` |
| Workspace | bind mount do repositório inteiro em `/workspace` |
| Usuário | UID/GID do usuário do host |
| Temporários | `HOME=/tmp`, caches em `/tmp` e `/tmp` como `tmpfs` efêmero |
| Rede | `ROADMAP_RUNTIME_NETWORK=none` por padrão |
| IPC | `ROADMAP_RUNTIME_IPC=host` por padrão |
| Imagem alternativa | `ROADMAP_RUNTIME_IMAGE=<imagem>` para imagem preparada com o mesmo contrato |
| Preflight | checagem interna de Docker daemon e imagem configurada antes de `docker run` |

Como o repositório é montado com escrita, qualquer comando executado pelo
wrapper pode criar, alterar ou remover arquivos do workspace. Antes de rodar
comandos que gerem artefatos, caches, relatórios, screenshots ou arquivos
versionáveis, aplique a política de confirmação vigente.

## Setup e preflight automático

`docker/runtime/run` executa o diagnóstico genérico de Docker daemon e imagem
configurada antes de chamar `docker run`. Quando um fluxo usa esse wrapper, o
agente não precisa rodar manualmente `docker version` nem
`docker image inspect` antes de cada uso do wrapper.

Se Docker não estiver pronto ou a imagem configurada não existir, o wrapper deve
falhar antes de executar o comando na imagem runtime, com mensagem clara. Esse
preflight é diagnóstico local e não autoriza pular a política de confirmação
para comandos que possam gerar artefatos, caches, relatórios, screenshots ou
arquivos versionáveis.

Se a imagem precisar ser criada ou reconstruída, use Docker CLI explicitamente:

```text
DOCKER_BUILDKIT=1 docker build \
  --tag my-roadmap-roadmap-runtime:playwright-1.60.0 \
  docker/runtime
```

Não resolva falhas instalando dependências no host, montando credenciais do
host, expondo o Docker socket, usando `--privileged` ou copiando manualmente o
comando interno do wrapper.

## Onde declarar comandos específicos

Comandos de validação mecânica, renderização, inspeção, extração, auditoria ou
geração pertencem à skill, spec ou documento que define aquele fluxo. Esses
documentos devem listar os comandos completos a serem executados via
`docker/runtime/run`, por exemplo:

```text
docker/runtime/run python3 <script> --flag <valor>
docker/runtime/run node <script> --flag <valor>
```

O wrapper deve continuar genérico mesmo quando vários fluxos usam a mesma
imagem runtime.
