# Runtime Docker e Makefile

<!-- AGENT-CARD START -->
Leia este documento ao alterar o runtime Docker, comandos que usam `docker/runtime/run`, dependências de execução do projeto ou targets do `Makefile`.
Use este documento para decidir o que pode rodar no host, o que deve rodar em imagem Docker e quando um target reutilizável do `Makefile` é justificado.
<!-- AGENT-CARD END -->

Esta convenção define como agentes devem usar o wrapper `docker/runtime/run`, manter as dependências fora do host e evoluir o `Makefile` sem transformar a interface operacional do repositório em uma lista de comandos descartáveis.

## Regra central

- Trate Docker, Node e Python como as únicas dependências esperadas no host quando forem exigidas por fluxos já contratados do repositório.
- Não instale ferramentas ad hoc no host para executar validações, gerar artefatos, renderizar páginas, baixar navegadores, compilar dependências nativas ou completar uma tarefa pontual.
- Coloque dependências adicionais na imagem runtime ou em uma imagem Docker específica.
- Use o `Makefile` como fachada reutilizável para comandos frequentes e estáveis, não como arquivo de atalhos para cada caso isolado.

## Quando usar `docker/runtime/run`

Use `docker/runtime/run` para comandos que dependem do ambiente runtime do projeto.

Isso inclui:

- validações mecânicas do repositório;
- comandos que dependem de Playwright, Chromium, navegadores ou bibliotecas de sistema empacotadas na imagem;
- scripts que esperam pacotes instalados na imagem runtime;
- comandos que precisam produzir resultado reprodutível entre máquinas;
- checks que geram artefatos, screenshots, relatórios, caches ou arquivos no workspace.

Não substitua o wrapper por `docker run` manual, instalação local de pacotes, `npm install` no host, `pip install` no host, download manual de binários ou execução direta de ferramenta que pertence à imagem.

## Quando usar Node ou Python no host

Node e Python podem rodar diretamente no host quando o comando pertencer a um fluxo do repositório que não faz parte do runtime Docker.

Use Python no host para:

- leitura, extração, transformação ou inspeção leve de artefatos estruturados;
- automações de publicação ou sincronização de documentação normativa quando o fluxo público do repositório exigir;
- inspeções locais que usem apenas a biblioteca padrão ou bibliotecas já disponíveis.

Use Node no host para:

- ferramentas de especificação, proposta ou automação que sejam contratadas fora da imagem runtime;
- inspeções leves que não dependam de pacotes do projeto, navegadores ou `node_modules` local.

Se o comando precisar instalar pacote, baixar runtime, usar navegador, compilar dependência nativa ou depender de versão de ferramenta que não está garantida no host, ele deve ir para Docker.

## Comportamento atual do wrapper

Considere estes detalhes como o contrato operacional atual do `docker/runtime/run` neste repositório:

| Aspecto | Comportamento |
|---|---|
| Imagem padrão | `my-roadmap-roadmap-runtime:playwright-1.60.0` |
| Build | `ROADMAP_RUNTIME_BUILD=missing`, `always` ou `never`; padrão `missing` |
| Diretório no contêiner | `/workspace` |
| Workspace | bind mount do repositório inteiro em `/workspace` |
| Usuário | UID/GID do usuário do host |
| Temporários | `HOME=/tmp`, caches em `/tmp` e `/tmp` como `tmpfs` efêmero |
| Rede | `ROADMAP_RUNTIME_NETWORK=none` por padrão |
| IPC | `ROADMAP_RUNTIME_IPC=host` por padrão |
| Entrada interativa | não configura `--interactive` nem `--tty`; prefira comandos não interativos |

Como o repositório é montado com escrita, qualquer comando no wrapper pode criar, alterar ou remover arquivos do workspace. Antes de rodar comandos que gerem artefatos, caches, relatórios, screenshots ou arquivos versionáveis, aplique a política de confirmação vigente.

## Imagem runtime ou imagem específica

Amplie a imagem runtime principal quando a dependência for:

- usada por vários comandos ou validações;
- pequena o bastante para não tornar a imagem difícil de manter;
- compatível com o ciclo de atualização do runtime principal;
- necessária para manter uma experiência uniforme entre agentes e máquinas.

Crie uma imagem Docker específica quando a dependência for:

- pesada, rara ou ligada a um fluxo isolado;
- privilegiada, sensível ou com requisitos próprios de rede, volume, usuário ou permissões;
- incompatível com o ciclo de atualização da imagem runtime principal;
- útil para separar responsabilidades ou reduzir risco de supply chain.

Em ambos os casos, registre versões, lockfiles ou digests quando aplicável e preserve cache de build sem depender de arquivos temporários versionados.

## Diagnóstico sem contornar o wrapper

Quando um comando falhar no runtime:

1. Leia a mensagem do comando chamado e identifique se a falha vem do script, do Docker ou da ausência da imagem.
2. Use `docker/runtime/run --build` quando a imagem precisar ser criada ou reconstruída.
3. Use `ROADMAP_RUNTIME_BUILD=always` para forçar rebuild quando a imagem local parecer defasada.
4. Use `ROADMAP_RUNTIME_BUILD=never` apenas quando quiser confirmar que a imagem já existe e evitar build automático.
5. Ajuste `ROADMAP_RUNTIME_IMAGE` somente para testar uma tag/imagem explicitamente preparada para o mesmo contrato.
6. Ajuste `ROADMAP_RUNTIME_NETWORK` ou `ROADMAP_RUNTIME_IPC` apenas quando o comando justificar essa exceção.

Não resolva falhas instalando dependências no host, montando credenciais do host, expondo o Docker socket, usando `--privileged` ou copiando comandos internos do wrapper sem necessidade explícita.

## Manutenção do `Makefile`

Adicione ou mantenha targets no `Makefile` quando o comando for:

- reutilizável por pessoas ou agentes;
- estável o bastante para fazer parte da interface operacional do repositório;
- parametrizável por variáveis claras como diretório, nível, identificador ou modo;
- melhor expresso como comando nomeado do que como instrução longa em documentação.

Prefira comando direto ou documentação quando o uso for único, experimental, altamente específico de um artefato local ou improvável de se repetir.

Targets operacionais devem:

- estar declarados em `.PHONY` quando não produzirem arquivo com o mesmo nome;
- usar nomes estáveis, descritivos e agrupados por domínio;
- validar variáveis obrigatórias antes de executar;
- mostrar mensagem de uso curta quando faltar parâmetro;
- chamar `docker/runtime/run` para comandos que pertencem ao runtime;
- reutilizar variáveis do próprio `Makefile` quando isso reduzir duplicação real.

Evite:

- targets para um único arquivo temporário, slug específico ou investigação pontual;
- aliases que só duplicam outro target sem clareza adicional;
- targets que escondem decisão semântica que o agente deveria tomar antes;
- comandos que instalam dependências no host;
- comandos longos duplicados em vários targets quando uma variável resolveria;
- targets que dependem de artefatos temporários não garantidos pelo fluxo normal do repositório.
