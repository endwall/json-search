VENV ?= venv
VENV_BIN ?= $(VENV)/bin

.PHONY: venv tests

default: venv

venv: venv/latest

venv/stable: stable-req.txt
	pip install virtualenv
	test -d $(VENV) || virtualenv-2.7 $(VENV) || virtualenv $(VENV)
	$(VENV_BIN)/pip install -Ur stable-req.txt
	@echo ""; echo "To activate your python environment run: source $(VENV_BIN)/activate"


venv/latest: requirements.txt
	pip install virtualenv
	test -d $(VENV) || virtualenv-2.7 $(VENV) || virtualenv $(VENV)
	$(VENV_BIN)/pip install -Ur requirements.txt
	@echo ""; echo "To activate your python environment run: source $(VENV_BIN)/activate"

venv/clean:
	rm -rf $(VENV)

clean:
	find . -name \*.py[oc] -exec rm -r {} \;

tests:
	nosetests -v --with-xunit

coverage:
	nosetests --with-coverage

lint:
	echo "" > flake8_output.txt
	flake8 --statistics --benchmark
	flake8_junit flake8_output.txt flake8_output_junit.xml

auto-lint:
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables jsearch tests
	isort --recursive --verbose
