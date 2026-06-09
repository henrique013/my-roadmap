# syntax=docker/dockerfile:1

FROM node:24-bookworm-slim

ENV ROADMAP_V2_RUNTIME_HOME=/opt/roadmap-v2/runtime \
    ROADMAP_V2_NODE_MODULES=/opt/roadmap-v2/runtime/node/node_modules \
    PLAYWRIGHT_BROWSERS_PATH=0 \
    PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium \
    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
    ASTRO_TELEMETRY_DISABLED=1 \
    PIP_NO_CACHE_DIR=1 \
    NPM_CONFIG_AUDIT=false \
    NPM_CONFIG_FUND=false \
    HOME=/tmp \
    XDG_CACHE_HOME=/tmp/.cache \
    TMPDIR=/tmp

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        chromium \
        fonts-liberation \
        fonts-noto-core \
        fonts-noto-color-emoji \
        python3 \
        python3-pip \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/roadmap-v2/skill

COPY requirements.txt /opt/roadmap-v2/skill/requirements.txt
RUN python3 -m venv /opt/roadmap-v2/runtime/python \
    && /opt/roadmap-v2/runtime/python/bin/python -m pip install --upgrade pip \
    && /opt/roadmap-v2/runtime/python/bin/python -m pip install -r /opt/roadmap-v2/skill/requirements.txt

COPY web/package.json web/package-lock.json /opt/roadmap-v2/skill/web/
RUN mkdir -p /opt/roadmap-v2/runtime/node \
    && cp /opt/roadmap-v2/skill/web/package.json /opt/roadmap-v2/runtime/node/package.json \
    && cp /opt/roadmap-v2/skill/web/package-lock.json /opt/roadmap-v2/runtime/node/package-lock.json \
    && cd /opt/roadmap-v2/runtime/node \
    && npm ci \
    && npm cache clean --force

COPY . /opt/roadmap-v2/skill/

RUN mkdir -p /opt/roadmap-v2/skill/tests /workspace/.tmp/roadmaps-v2 /workspace/input /workspace/fixtures /workspace/llm-outputs /tmp/.cache \
    && find /opt/roadmap-v2 -type d -name __pycache__ -prune -exec rm -rf {} + \
    && chmod -R a+rX /opt/roadmap-v2 /workspace \
    && chmod 1777 /tmp

ENTRYPOINT ["/opt/roadmap-v2/runtime/python/bin/python", "-B", "/opt/roadmap-v2/skill/scripts/run_pipeline.py"]
