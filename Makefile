ROADMAP_V2_IMAGE ?= roadmap-v2-runner:local
ROADMAP_V2_SKILL_SOURCE ?= templates/skills-local/roadmap-v2

.PHONY: setup
setup: roadmap-v2-image roadmap-v2-clean-legacy-runtime

.PHONY: roadmap-v2-image
roadmap-v2-image:
	docker build \
		-t "$(ROADMAP_V2_IMAGE)" \
		-f "$(ROADMAP_V2_SKILL_SOURCE)/Dockerfile" \
		"$(ROADMAP_V2_SKILL_SOURCE)"

.PHONY: roadmap-v2-test-container
roadmap-v2-test-container:
	docker run --rm \
		--network none \
		--read-only \
		--tmpfs /tmp:rw,exec,nosuid,size=1024m,mode=1777 \
		--entrypoint /opt/roadmap-v2/runtime/python/bin/python \
		--mount type=bind,source="$(CURDIR)/$(ROADMAP_V2_SKILL_SOURCE)/tests",target=/opt/roadmap-v2/skill/tests,readonly \
		"$(ROADMAP_V2_IMAGE)" \
		-B /opt/roadmap-v2/skill/scripts/run_tests.py --mode all

.PHONY: roadmap-v2-clean-legacy-runtime
roadmap-v2-clean-legacy-runtime:
	@echo "Removing generated legacy roadmap-v2 runtimes, if present."
	rm -rf .codex-runtime/roadmap-v2 .codex/runtime/roadmap-v2
