include ./configuration.mk
include ./common.mk

SHELL:=/bin/bash

pre-commit:
	$(MAKE) test
.PHONY: pre-commit

pre-push:
	@echo "Nothing to do"
.PHONY: pre-push


dist:
	chmod +x dist.sh
	./dist.sh
.PHONY: dist
TMP_FOLDER := /tmp

test: typecheck
	@ls -d spec/fake_libc_include/
	date
	mamba
	date
.PHONY: test

typecheck:
	mypy . --config-file mypy.ini
.PHONY: typecheck

clean-ignored-files:
	git clean -xdf test || true # allow failure in CI
.PHONY: clean-ignored-files

