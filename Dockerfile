FROM python:3.6-slim-stretch

COPY ./ /var/cache/salt-confd/

RUN mkdir -p /etc/salt/confd/conf.d /etc/salt/confd/templates

RUN apt-get update \
 && apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
  && pip --no-cache-dir install /var/cache/salt-confd/ \
  && rm -rf /var/cache/salt-confd/ \
  && apt-get remove -y build-essential libssl-dev libffi-dev \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*
