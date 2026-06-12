# 0001 - Usar Astro Starlight como driver frontend da skill de roadmap

Status: Aceita

Data: 2026-06-12

## Contexto

A skill de roadmap está em transição para uma nova versão. A versão antiga gera páginas estáticas em HTML/CSS puro, linkadas entre si, com bom tom narrativo para conteúdos técnicos, mas com apresentação visual amadora e mistura entre produto final e artefatos editoriais usados para gerar as páginas.

A nova versão deve preservar a simplicidade e o caráter estático do resultado, mas precisa entregar uma experiência visual mais profissional e consistente. O roadmap final deve funcionar como uma documentação narrativa, com tom de livro técnico guiado, não como aplicação interativa.

Também foi definida uma regra importante: os roadmaps devem ser expressos com componentes oficiais documentados da biblioteca escolhida. Componentes customizados para representar a linguagem do roadmap devem ser evitados como regra de arquitetura, não apenas como preferência.

## Padrão de ADR usado

Não foi encontrada uma RFC específica que defina a estrutura de ADRs. A referência formal mais próxima é a ISO/IEC/IEEE 42010:2022, que trata de descrição de arquitetura, mas não define formato ou mídia para registrar uma descrição de arquitetura.

Esta ADR usa uma estrutura leve baseada no padrão de Michael Nygard, com contexto, decisão, status e consequências, complementada por campos do MADR para registrar drivers, opções consideradas e confirmação.

## Drivers da decisão

- O driver principal deve ser um gerador estático orientado a páginas, dados e templates.
- O conteúdo editorial deve ficar separado da saída publicada, em estrutura como `src/`.
- A saída oficial deve ser uma pasta estática limpa, como `dist/`.
- A experiência alvo é desktop, narrativa e documental, sem interatividade complexa.
- Mobile e TV não são superfícies prioritárias e não devem orientar a otimização do roadmap gerado.
- A base visual deve ter componentes oficiais documentados suficientes para expressar conteúdo técnico.
- O conjunto de componentes deve cobrir, no mínimo, blocos de código, tabelas, callouts, etapas, abas, cartões, navegação e árvores de arquivos.
- A solução deve priorizar maturidade e previsibilidade, sem forçar customização visual ad hoc.
- A integração com geração automatizada de roadmaps deve ser simples e auditável.

## Opções consideradas

| Opção | Avaliação |
|---|---|
| Astro Starlight | Melhor encaixe geral. Combina Astro, geração estática, estrutura `src/content/docs/`, saída `dist/` e componentes oficiais para documentação técnica. |
| Docusaurus | Muito maduro e forte para documentação, mas menos alinhado à regra de expressar a linguagem do roadmap apenas com componentes oficiais prontos. |
| Nextra | Tem componentes documentais úteis, mas puxa o projeto para Next/React e aumenta a complexidade operacional para uma saída estática simples. |
| Material for MkDocs | Maduro para documentação técnica, mas muda o stack para Python/MkDocs e não encaixa tão diretamente na direção de frontend estático da skill. |
| VitePress | Simples para documentação, mas menos aderente ao conjunto específico de componentes esperado para os roadmaps. |
| Eleventy com Bootstrap ou CSS puro | Simples e estático, mas tende a recriar a linguagem visual própria que a nova versão quer evitar. |

## Decisão

Usaremos Astro Starlight como driver do frontend gerado pela skill de roadmap.

Astro Starlight será a base para estruturar o conteúdo-fonte em área editorial separada, gerar uma saída estática limpa em `dist/` e fornecer a linguagem de componentes oficial para representar roadmaps narrativos técnicos.

A decisão inclui as seguintes regras:

- O produto final publicado deve ser uma pasta estática limpa, como `dist/`.
- O conteúdo-fonte e editorial deve ficar fora do output publicado, em estrutura como `src/`.
- A experiência gerada deve permanecer documental e narrativa, sem se transformar em aplicação interativa.
- A experiência gerada deve ser otimizada para desktop, não para mobile ou TV.
- Os componentes usados para expressar o roadmap devem ser componentes oficiais documentados do Starlight ou do ecossistema Astro adotado explicitamente.
- Componentes customizados para a linguagem principal do roadmap não fazem parte da decisão aceita.

## Justificativa

Starlight é a opção que melhor combina o modelo desejado de entrega com a regra de não criar componentes próprios para a linguagem do roadmap.

A documentação oficial do Starlight lista componentes embutidos para casos comuns de documentação, incluindo cartões, asides, badges, código, árvores de arquivos, ícones, botões de link, etapas e abas. Esses componentes cobrem diretamente os elementos esperados para roadmaps técnicos narrativos.

O Starlight também organiza páginas a partir de `src/content/docs/`, onde arquivos `.md`, `.mdx` ou `.mdoc` viram páginas do site. O Astro oferece servidor de desenvolvimento com atualização em mudanças de `src/` e build para uma pasta `dist/` por padrão.

Docusaurus foi mantido como principal alternativa por maturidade, mas perdeu para Starlight neste contexto porque a decisão prioriza a cobertura oficial de componentes documentais necessários ao roadmap mais do que a maturidade histórica da plataforma.

## Consequências

Consequências positivas:

- A nova versão passa a ter uma base visual documentada, consistente e menos dependente de decisões visuais ad hoc.
- A separação entre fonte editorial e saída publicada fica alinhada ao modelo `src/` -> `dist/`.
- A skill pode gerar documentação narrativa técnica usando componentes oficiais adequados a código, etapas, abas, árvores de arquivos, callouts e cartões.
- A experiência local de desenvolvimento fica compatível com um fluxo simples de servidor local e build estático.

Consequências negativas ou riscos:

- A decisão introduz dependência direta do ecossistema Astro/Starlight.
- Starlight é menos historicamente consolidado que Docusaurus.
- A regra de não criar componentes customizados pode limitar certos formatos visuais caso eles não existam oficialmente.
- A adoção deve ser revisitada se a biblioteca deixar de cobrir componentes essenciais para o roadmap ou se o ecossistema reduzir manutenção.

Consequências neutras:

- A decisão não exige interatividade avançada no cliente.
- A decisão pode herdar comportamento responsivo básico do Starlight, mas mobile e TV não serão critérios principais de design ou validação.
- A decisão não define ainda a implementação concreta da skill, os scripts de geração, o formato exato dos dados de entrada ou a organização final dos templates.
- A decisão não impede customização de tema suportada oficialmente, desde que isso não crie componentes próprios para expressar conteúdo do roadmap.

## Confirmação

A conformidade com esta ADR será avaliada por revisão dos artefatos futuros da skill de roadmap.

Uma implementação estará alinhada a esta decisão quando:

- gerar uma saída estática limpa em `dist/` ou equivalente;
- manter conteúdo-fonte, dados e material editorial fora do output publicado;
- usar Astro Starlight como base do frontend gerado;
- representar a linguagem principal do roadmap com componentes oficiais documentados;
- validar a experiência principalmente em desktop;
- preservar a experiência de documentação narrativa técnica, sem transformar o roadmap em aplicação interativa.

## Referências

- ISO/IEC/IEEE 42010:2022 - Software, systems and enterprise - Architecture description: https://www.iso.org/standard/74393.html
- Michael Nygard - Documenting Architecture Decisions: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- MADR - Markdown Architectural Decision Records: https://adr.github.io/madr/
- Thoughtworks Technology Radar - Lightweight Architecture Decision Records: https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records
- Starlight - Using Components: https://starlight.astro.build/components/using-components/
- Starlight - Project Structure: https://starlight.astro.build/guides/project-structure/
- Astro - Develop and build: https://docs.astro.build/en/develop-and-build/
