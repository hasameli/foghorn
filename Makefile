clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +
	rm -rf build

lint:
	flake8

run:
	python foghorn.py

all: clean
	python setup.py build

install: all
	python setup.py install
