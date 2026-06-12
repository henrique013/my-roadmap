> Arquivo gerado. Não edite manualmente.
> Altere a fonte e o manifesto aplicáveis e use o fluxo público de publicação do repositório.

# Runtime Docker Aberto

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
- repassar o comando recebido sem interpretar flags de domínio.

O wrapper não deve:

- validar variáveis de fluxos específicos, como `ROADMAP_DIR`, `LEVEL` ou
  `NODE`;
- ter catálogo de targets;
- ter modo de build;
- ter modo de preflight;
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

Como o repositório é montado com escrita, qualquer comando executado pelo
wrapper pode criar, alterar ou remover arquivos do workspace. Antes de rodar
comandos que gerem artefatos, caches, relatórios, screenshots ou arquivos
versionáveis, aplique a política de confirmação vigente.

## Setup e diagnóstico explícitos

Antes de depender da imagem runtime, o fluxo responsável deve declarar os
comandos de diagnóstico que precisa. Para o runtime padrão:

```text
docker version
docker image inspect my-roadmap-roadmap-runtime:playwright-1.60.0
```

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
