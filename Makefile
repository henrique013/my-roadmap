.PHONY: setup roadmap-runtime-build roadmap-runtime-check roadmap-roadmap-html-shape roadmap-roadmap-artifacts roadmap-roadmap-visual-check roadmap-node-html-shape roadmap-node-artifacts roadmap-node-visual-check roadmap-roadmap-visual-check-test

setup:
	@docker/runtime/run --build

roadmap-runtime-build:
	@docker/runtime/run --build

roadmap-runtime-check:
	@docker/runtime/run --preflight

roadmap-roadmap-html-shape:
	@test -n "$(ROADMAP_DIR)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug>"; exit 2; }
	@docker/runtime/run python3 .codex/skills/roadmap/roadmap-page/scripts/check_roadmap_html_shape.py --html "$(ROADMAP_DIR)/roadmap.html"

roadmap-roadmap-artifacts:
	@test -n "$(ROADMAP_DIR)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug>"; exit 2; }
	@docker/runtime/run python3 .codex/skills/roadmap/roadmap-page/scripts/validate_roadmap_artifacts.py --roadmap-dir "$(ROADMAP_DIR)"

roadmap-roadmap-visual-check:
	@test -n "$(ROADMAP_DIR)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug>"; exit 2; }
	@docker/runtime/run node .codex/skills/roadmap/roadmap-page/scripts/check_roadmap_visual_render.mjs --roadmap-dir "$(ROADMAP_DIR)"

roadmap-node-html-shape:
	@test -n "$(NODE_DIR)" || { echo "Use: make $@ NODE_DIR=.tmp/roadmaps/<slug>/<level>/<node-slug>"; exit 2; }
	@docker/runtime/run python3 .codex/skills/roadmap/node-pages/scripts/check_html_shape.py --html "$(NODE_DIR)/node.html"

roadmap-node-artifacts:
	@test -n "$(ROADMAP_DIR)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@test -n "$(LEVEL)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@test -n "$(NODE)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@docker/runtime/run python3 .codex/skills/roadmap/node-pages/scripts/validate_node_artifacts.py --roadmap-dir "$(ROADMAP_DIR)" --level "$(LEVEL)" --node "$(NODE)"

roadmap-node-visual-check:
	@test -n "$(ROADMAP_DIR)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@test -n "$(LEVEL)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@test -n "$(NODE)" || { echo "Use: make $@ ROADMAP_DIR=.tmp/roadmaps/<slug> LEVEL=<level> NODE=<node-slug>"; exit 2; }
	@docker/runtime/run node .codex/skills/roadmap/node-pages/scripts/check_visual_render.mjs --roadmap-dir "$(ROADMAP_DIR)" --level "$(LEVEL)" --node "$(NODE)"

roadmap-roadmap-visual-check-test:
	@docker/runtime/run node .codex/skills/roadmap/roadmap-page/scripts/test_check_roadmap_visual_render.mjs
