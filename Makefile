# Installing:
# pip install black isort autoflake

default: help
.PHONY: default

reformat:
	$(eval FILES := $(filter-out $@,$(MAKECMDGOALS)))
	@if [ -z "$(FILES)" ]; then \
		files=$$(git status --short | awk '/\.py$$/{if ($$1 != "D" && $$1 != " D") print substr($$0, index($$0, $$2))}'); \
	else \
		files=$(FILES); \
	fi; \
	if [ -n "$$files" ]; then \
		autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place $$files --exclude=__init__.py --exclude=apps.py;\
		black $$files; \
		isort $$files; \
	else \
		echo "No Python files to process."; \
	fi
.PHONY: reformat
