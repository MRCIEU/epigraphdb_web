.PHONY: clean

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = epigraphdb_web

ifndef WEBAPI_PORT
WEBAPI_PORT=8006
endif

ifndef DEBUG
DEBUG=false
endif

#################################################################################
# Rules
#################################################################################

## ==== utils ====
__utils__:

## Unit tests
test:
	python -m pytest -v

## ==== codebase ====
__codebase__:

## Lint codebase (flake8, mypy)
lint:
	python -m flake8 app tests
	python -m mypy app tests

## Format codebase (black, isort)
fmt:
	python -m autoflake --in-place --remove-all-unused-imports --recursive app tests
	python -m isort -rc app tests
	python -m black app tests

## Start API server, default to 8000, overwrite with WEBAPI_PORT make run
run:
	uvicorn app.main:app --reload \
	--port ${WEBAPI_PORT}

## Start API server using port 80 (for docker)
run80:
	uvicorn app.main:app --reload \
	--host 0.0.0.0 --port 80


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$$(tput bold)Params:$$(tput sgr0)"
	@echo
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}'
