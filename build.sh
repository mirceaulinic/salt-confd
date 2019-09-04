#!/bin/sh

apt-get install ruby ruby-dev rubygems build-essential
gem install --no-ri --no-rdoc fpm

fpm -s python -t rpm --python-package-name-prefix python26 setup.py
fpm -s python -t deb --python-package-name-prefix python26 setup.py
fpm -s python -t rpm --python-package-name-prefix python36 setup.py
fpm -s python -t deb --python-package-name-prefix python36 setup.py
fpm -s python -t rpm --python-package-name-prefix python37 setup.py
fpm -s python -t deb --python-package-name-prefix python37 setup.py
