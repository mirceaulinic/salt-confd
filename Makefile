VERSION ?= $(shell git describe --tags --always --dirty="-dev")
SALT_VERSION ?= 2019.2.0
IMAGE ?= mirceaulinic/salt-confd
TAG ?= $(IMAGE):$(VERSION)

release:
	rm -rf dist
	rm -rf docs/_build/
	# cd docs && make man && cd ..
	python setup.py sdist
	python3 setup.py sdist
	twine upload dist/* --skip

build:
	docker build -f Dockerfile . -t $(TAG) --build-arg SALT_VERSION=$(SALT_VERSION)

black:
	black --check --skip-string-normalization .

format:
	black --skip-string-normalization .
