# syntax=docker/dockerfile:1.7

FROM mcr.microsoft.com/playwright:v1.60.0-noble@sha256:9bd26ad900bb5e0f4dee75839e957a89ae89c2b7ab1e76050e559790e946b948

ENV NODE_ENV=production \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_FUND=false \
    NPM_CONFIG_UPDATE_NOTIFIER=false \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

USER root

RUN bash --version >/dev/null \
    && python3 --version \
    && node --version \
    && npm --version \
    && grep --version >/dev/null \
    && sed --version >/dev/null \
    && find --version >/dev/null

WORKDIR /opt/roadmap-runtime

COPY package.json package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev \
    && ln -s /opt/roadmap-runtime/node_modules /node_modules \
    && node -e "const { chromium } = require('playwright'); console.log(chromium.name())" \
    && python3 --version

WORKDIR /workspace
