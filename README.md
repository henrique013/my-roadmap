# My Roadmap

`my-roadmap` existe para criar roadmaps de aprendizado customizados.

A ideia do projeto é transformar um objetivo de aprendizado em uma trilha
navegável: o que vem antes, o que depende de quê e qual caminho faz sentido
seguir para dominar um assunto.

## Estado Atual

A skill de geração anterior foi removida temporariamente para que uma nova
skill possa ser criada do zero em uma etapa futura.

Neste estado intermediário, o repositório mantém:

- a ideia e o escopo do projeto;
- o manifesto de composição de instruções;
- o fluxo público de sincronização de documentação e skills;
- o ferramental Docker/runtime usado pelo projeto.

Não há, nesta etapa, uma interface publicada para gerar novos roadmaps ou
páginas profundas de nodes.

## Ferramental

O runtime Docker do projeto permanece preservado. Ele continua disponível para
fluxos futuros que precisem de um ambiente isolado com Node.js, Python 3,
Playwright, Chromium e dependências de navegador.

O wrapper `docker/runtime/run` também permanece como fachada genérica para
executar comandos dentro da imagem runtime configurada. Ele não define, por si
só, um workflow de geração.

## Próxima Etapa

A próxima etapa planejada é criar uma nova skill de geração do zero, sem
reaproveitar automaticamente a implementação anterior.

Até essa nova skill existir, este repositório deve ser tratado como base de
projeto e ferramental, não como ferramenta operacional de geração de roadmaps.
