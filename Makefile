.PHONY: install upload doc clean re

DOC_DIR = docs

PYCACHE = $(shell find * -name __pycache__ -type d)


install:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

doc:
	mkdir -p $(shell pwd)/$(DOC_DIR)/_static
	mkdir -p $(shell pwd)/$(DOC_DIR)/_templates
	@(cd $(DOC_DIR) && $(MAKE) html)

venv:
	virtualenv --python=python3 venv
	venv/bin/pip install dist/dataf-0.0.3.tar.gz
	venv/bin/pip install psycopg2-binary
	venv/bin/pip install codecov

test:
	venv/bin/python -m unittest $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

cov:
	venv/bin/coverage run -m unittest discover
	venv/bin/coverage html

clean:
	@rm -rf dist
	@rm -rf build
	@rm -rf dataf.egg-info
	@rm -rf .eggs
	@rm -rf .pytest_cache
	@rm -rf .tox
	@rm -rf coverage.xml
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf docs/_build/
	@rm -rf docs/_static/
	@rm -rf docs/_templates/
	@rm -rf venv
	@rm -rf $(PYCACHE)

re: clean install
