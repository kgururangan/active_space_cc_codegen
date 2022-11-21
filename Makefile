.DEFAULT_GOAL := install
src := actgen

.PHONY: install
install:
	$(CONDA_PREFIX)/bin/pip install -e .

.PHONY: check-dist
check-dist:
	python setup.py check -ms
	python setup.py sdist
	twine check dist/*
