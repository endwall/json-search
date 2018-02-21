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
	find . -name "*.json-result" -type f -delete
	nosetests -v --with-xunit
	for f in $$(find . -name '*.json' | grep '/fixtures/'); do if [ ! -f "$${f}-result" ]; then echo "removing" $${f}; rm $${f}; fi; done

coverage:
	nosetests --with-coverage

lint:
	echo "" > flake8_output.txt
	flake8 --statistics --benchmark
	flake8_junit flake8_output.txt flake8_output_junit.xml

auto-lint:
	autoflake --recursive --in-place --remove-all-unused-imports --remove-unused-variables common tests sb_blueprints projects
	isort --recursive --verbose
