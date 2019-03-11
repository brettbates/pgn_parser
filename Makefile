.PHONY: build

build:
	python3 setup.py sdist bdist_wheel

push:
	twine upload dist/*
