# 0002 - Usar template Starlight com workspace temporário por roadmap

Status: Aceita

Data: 2026-06-12

## Contexto

A ADR 0001 decidiu usar Astro Starlight como driver frontend da nova versão da skill de roadmap. Essa decisão definiu que os roadmaps devem ser documentação narrativa técnica, com foco em desktop, componentes oficiais documentados e saída estática limpa em `dist/`.

Depois dessa escolha, surgiu uma decisão arquitetural complementar: como incorporar Astro Starlight ao fluxo de uma skill que gera roadmaps automaticamente.

Astro Starlight não é apenas uma folha de estilo ou um conjunto avulso de componentes HTML. Ele pressupõe um projeto Astro completo durante a geração e produz uma saída estática publicável em `dist/`.

A versão antiga da skill gerava HTML/CSS puro diretamente e misturava, na mesma árvore de resultado, páginas finais, pesquisa editorial, contratos, auditorias, screenshots e artefatos de pipeline. A nova arquitetura deve evitar essa mistura.

## Drivers da decisão

- O roadmap final deve ser uma pasta estática limpa, como `dist/`.
- O usuário final não deve receber um projeto Astro/Starlight completo como artefato principal.
- O projeto Astro/Starlight deve ser infraestrutura de geração, não produto final.
- O conteúdo-fonte, material editorial, contratos, auditorias e artefatos intermediários devem ficar fora do output publicável.
- A skill deve continuar capaz de gerar múltiplos roadmaps sem acoplar cada roadmap à raiz do repositório.
- A arquitetura deve preservar simplicidade operacional e evitar overengineering.
- O uso de componentes oficiais do Starlight deve continuar centralizado e controlado pela skill.

## Opções consideradas

| Opção | Avaliação |
|---|---|
| Projeto Astro/Starlight fixo na raiz do repositório | Útil para desenvolvimento do template, mas acopla a skill ao repositório, polui a raiz e não representa bem múltiplos roadmaps. |
| Projeto Astro/Starlight isolado por roadmap entregue ao usuário | Facilita edição manual posterior, mas entrega dependências, configuração e fonte junto do produto final; contraria a meta de saída limpa. |
| Template Starlight dentro da skill | Mantém a skill autocontida e centraliza configuração, dependências e linguagem visual, mas precisa de um local de materialização para build. |
| Workspace temporário de build por roadmap | Isola a geração, evita poluir a raiz e permite entregar apenas `dist/`, mas exige contrato claro de separação entre fonte, build e output. |
| Template Starlight versionado pela skill com workspace temporário por roadmap | Combina controle centralizado do template com isolamento por roadmap e saída final limpa. |

## Decisão

Usaremos um template Astro/Starlight versionado pela skill de roadmap, materializado em um workspace temporário de build para cada roadmap gerado.

Cada roadmap não será entregue como um projeto Astro/Starlight isolado. O projeto Astro completo existirá apenas como infraestrutura de geração.

A arquitetura conceitual será uma separação em três árvores: template
versionado, workspace temporário e output publicável.

Os nomes abaixo ilustram a forma da arquitetura; a implementação pode decidir
os caminhos finais.

```text
skill-roadmap/
├── starlight-template/
│   ├── package.json
│   ├── astro.config.*
│   ├── public/
│   └── src/
│       └── fonte Starlight base
│
└── gerador da skill

workspace-temporario-do-roadmap/
├── projeto-starlight-materializado/
│   ├── package.json
│   ├── astro.config.*
│   ├── public/
│   └── src/
│       └── conteúdo gerado do roadmap
│
├── editorial-e-auditoria/
│   ├── pesquisa
│   ├── contratos
│   ├── dumps
│   └── relatórios
│
└── dist/
    ├── index.html
    ├── páginas do roadmap
    └── assets
```

A separação de responsabilidades será:

| Camada | Responsabilidade | Publicável |
|---|---|---:|
| Template Starlight | Projeto-base controlado pela skill, com configuração, dependências, tema permitido e uso de componentes oficiais. | Não |
| Fonte gerada | Conteúdo do roadmap convertido para uma estrutura compatível com Starlight. | Não |
| Workspace temporário | Projeto Astro completo materializado para gerar um roadmap específico. | Não |
| Artefatos editoriais e de auditoria | Pesquisa, contratos, dumps, relatórios, screenshots e evidências de pipeline. | Não |
| `dist/` final | Site estático compilado, com HTML, CSS, JavaScript e assets necessários para deploy. | Sim |

A fronteira principal da decisão é simples: o que estiver acima de `dist/`
serve para construir ou explicar o roadmap; o que estiver dentro de `dist/` é o
site estático publicável.

## Justificativa

Essa arquitetura preserva a simplicidade do produto final sem negar a natureza real do Astro Starlight.

Como Starlight pressupõe um projeto Astro, a skill precisa materializar um projeto completo para executar o build. Porém, esse projeto não deve ser confundido com o roadmap entregue. Ele é apenas a oficina temporária onde o site é montado.

O template versionado pela skill centraliza as escolhas visuais, o conjunto de componentes oficiais permitidos e a configuração do Starlight. O workspace temporário permite injetar o conteúdo específico de cada roadmap sem poluir a raiz do repositório e sem transformar cada roadmap em um projeto próprio.

O `dist/` final passa a ser a fronteira clara entre produto publicável e bastidores da geração.

## Consequências

Consequências positivas:

- A entrega final fica limpa, publicável e separada dos artefatos editoriais.
- A skill mantém controle centralizado sobre Starlight, configuração, dependências e linguagem visual.
- Cada roadmap pode ser gerado de forma isolada sem criar um projeto permanente próprio.
- A arquitetura evita repetir o problema antigo de misturar páginas finais com pesquisa, contratos e auditorias.
- A geração de múltiplos roadmaps fica mais previsível, pois cada build pode usar um workspace separado.

Consequências negativas ou riscos:

- A skill passa a depender de uma etapa de materialização de projeto antes do build.
- O template Starlight precisa ser mantido junto com as versões de Astro/Starlight adotadas.
- A separação entre fonte, workspace temporário, artefatos editoriais e `dist/` precisa ser respeitada de forma consistente.
- Debug de problemas visuais pode exigir inspeção do workspace temporário, não apenas do `dist/`.

Consequências neutras:

- Um projeto Starlight fixo na raiz pode existir apenas se for decidido futuramente como ambiente auxiliar de desenvolvimento, mas ele não é o modelo de geração nem o artefato entregue.
- A decisão não define os nomes finais dos diretórios internos da skill.
- A decisão não define ainda os comandos, scripts ou contratos exatos de build.

## Confirmação

Uma implementação estará alinhada a esta ADR quando:

- mantiver um template Astro/Starlight controlado pela skill;
- materializar um workspace de build por roadmap;
- gerar o conteúdo do roadmap como fonte Starlight antes do build;
- entregar como output publicável apenas o `dist/` ou equivalente;
- mantiver conteúdo editorial, contratos, auditorias e artefatos intermediários fora do `dist/`;
- não entregar cada roadmap como um projeto Astro/Starlight completo, salvo decisão futura explícita.

## Referências

- ADR 0001 - Usar Astro Starlight como driver frontend da skill de roadmap: `docs/adrs/0001-usar-astro-starlight-como-driver-frontend-da-skill-roadmap.md`
- Astro - Project Structure: https://docs.astro.build/en/basics/project-structure/
- Astro - Develop and build: https://docs.astro.build/en/develop-and-build/
- Astro - Configuration Reference: https://docs.astro.build/en/reference/configuration-reference/
- Starlight - Getting Started: https://starlight.astro.build/getting-started/
- Starlight - Project Structure: https://starlight.astro.build/guides/project-structure/
- Starlight - Using Components: https://starlight.astro.build/components/using-components/
