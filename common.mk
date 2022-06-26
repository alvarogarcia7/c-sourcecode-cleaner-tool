SHELL:=/bin/bash

install: virtualenv-create install-requirements install-githooks
.PHONY: install

virtualenv-create:
	${PYTHON} -m venv ./venv
.PHONY: virtualenv-create

virtualenv-clean:
	rm -rf ./venv
.PHONY: virtualenv-clean

requirements.txt:
	${PIP} freeze > requirements.txt
.PHONY: requirements.txt

install-requirements: check-virtual-env
	${PIP} install -r requirements.txt
.PHONY: install-requirements

install-githooks:
	pre-commit install
.PHONY: install-githooks

check-virtual-env:
	@# Test if the variable is set
	@if [ -z "${VIRTUAL_ENV}" ]; then                                               \
  		echo "Need to activate virtual environment: source ./venv/bin/activate";    \
  		false;       																\
  	fi

