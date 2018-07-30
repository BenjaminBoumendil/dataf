.PHONY: install upload doc clean re

DOC_DIR = docs

UPLOAD_URL = https://test.pypi.org/legacy/


install:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload --repository-url $(UPLOAD_URL) dist/*

doc:
	mkdir -p $(shell pwd)/$(DOC_DIR)/_static
	mkdir -p $(shell pwd)/$(DOC_DIR)/_templates
	@(cd $(DOC_DIR) && $(MAKE) html)

clean:
	rm -rf dist
	rm -rf build
	rm -rf dataf.egg-info
	rm -rf .eggs
	rm -rf .pytest_cache
	rm -rf .tox
	rm -rf coverage.xml
	rm -rf .coverage

re: clean all
