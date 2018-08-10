.PHONY: install upload doc clean re

DOC_DIR = docs

UPLOAD_URL = https://test.pypi.org/legacy/

TESTS_DIR = dataf.tests.


install:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload --repository-url $(UPLOAD_URL) dist/*

doc:
	mkdir -p $(shell pwd)/$(DOC_DIR)/_static
	mkdir -p $(shell pwd)/$(DOC_DIR)/_templates
	@(cd $(DOC_DIR) && $(MAKE) html)

venv:
	virtualenv --python=python3 venv
	venv/bin/pip install dist/dataf-0.0.1.tar.gz
	venv/bin/pip install psycopg2-binary
	venv/bin/pip install codecov

test:
	venv/bin/python -m unittest $(TESTS_DIR)$(filter-out $@,$(MAKECMDGOALS))

%:
	@:

cov:
	venv/bin/coverage run -m unittest discover
	venv/bin/coverage html

clean:
	rm -rf dist
	rm -rf build
	rm -rf dataf.egg-info
	rm -rf .eggs
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf coverage.xml
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf docs/_build/
	rm -rf docs/_static/
	rm -rf docs/_templates/
	rm -rf **/__pycache__
	rm -rf venv

re: clean install
