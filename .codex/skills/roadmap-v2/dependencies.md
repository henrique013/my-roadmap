# Dependencias do Roadmap V2

Data de avaliacao: 2026-06-08

## Python

| Componente | Versao | Classe | Evidencia | Motivo | Rollback |
|---|---:|---|---|---|---|
| `pydantic` | `2.13.4` | minor/patch | PyPI lista `v2.13.4` como release de 2026-05-06 | Modelos internos estritos e exportacao de JSON Schema | Voltar para a versao anterior pinada em `requirements.txt` e regenerar schemas |
| `jsonschema` | `4.26.0` | minor | PyPI lista `4.26.0` como release estavel | Validacao externa de schemas persistidos | Voltar para a versao anterior pinada e manter validacao Pydantic interna |
| `PyYAML` | `6.0.3` | patch | PyPI/registry publico lista `6.0.3` | Leitura de `pipe.yaml` e manifests de pipeline | Voltar para `6.0.1` ja presente no host se houver regressao |
| `beautifulsoup4` | `4.14.3` | minor | PyPI/conda indicam `4.14.3` como release estavel de 2026 | Validacao DOM deterministica | Voltar para `4.12.3` ja presente no host se houver regressao |

## Node e renderer

| Componente | Versao | Classe | Evidencia | Motivo | Rollback |
|---|---:|---|---|---|---|
| `astro` | `6.4.4` | minor | `npm view astro version` em 2026-06-08 | Renderer estatico de `PageSpec` | Voltar para a versao pinada anterior do `web/package.json` |
| `@awesome.me/webawesome` | `3.8.0` | minor | Documentacao oficial do Web Awesome mostra `v3.8.0`; `npm view` confirmou | Biblioteca documentada de componentes web | Voltar para a versao pinada anterior e recopiada para a saida renderizada |
| `playwright` | `1.60.0` | minor | Lockfile do renderer pinado em `web/package-lock.json` | Gates visuais locais com Chromium | Voltar para a versao pinada anterior e reinstalar o runtime da skill |
| `typescript` | `6.0.3` | major para novo workspace | `npm view typescript version` em 2026-06-08 | Tipagem do renderer Astro | Voltar para `5.9.x` se o build Astro apontar incompatibilidade |

## Observacoes

- O renderer v2 fica dentro do pacote publicado da skill em `<skill-dir>/web/`.
- Web Awesome deve ser servido localmente. O build nao deve depender de CDN.
- Os assets devem ser copiados do pacote pinado para `RENDER_OUTPUT_DIR/vendor/webawesome/dist-cdn/`.
- Validacao de integracao deve falhar quando dependencias ainda nao estiverem instaladas.
- `@astrojs/check@0.9.9` foi avaliado em 2026-06-08, mas removido antes da
  finalizacao porque `npm audit` apontou 5 vulnerabilidades moderadas transitivas
  via `yaml-language-server`. Como o renderer precisa apenas de build estatico,
  manter o componente de diagnostico aumentaria superficie sem necessidade.
- Apos remover `@astrojs/check`, o lockfile do renderer
  reportou `found 0 vulnerabilities`.
