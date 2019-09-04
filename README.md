# salt-confd

Lightweight Salt package à la [confd](https://github.com/kelseyhightower/confd)
management of local application configuration files.

Why
---

Please note that the intent of this software package is not to compete against
``confd`` or other popular equivalents; it was born purely out of my personal
preference / bias of using Salt for managing files (and others). Salt is
typically at the opposite end of "lightweight" and this package aims to
alleviate this, however it still cannot get better than ``confd`` - from this
perspective. Alas, it's written in Python (please let's not have this discussion
over here 😄).

In short, here's why I took this approach:

* Why not? It's fun.
* I like Salt, and it offers a variety of well-known templating languages to
  manage the files, including Jinja, Mako, Cheetah, or even pure Python - and
  others. In other words, I find that I prefer to use something I'm already
  comfortable with, particularly in environments where Salt is already a
  requirement.
* What I find missing in ``confd`` is the possibility to manage the local config
  files based on more environment parameters - e.g., have idempotent templates
  that can be used across a number of distributions (as in opposite to having
  separate files / directory tree / or even repositories for different
  base operating system distribution); with Salt, this can be very easily done
  using the Grains.
* Salt covers a large variety of backends to fetch the data from (including 
  Redis, Vault, Consul, etcd, and so on).
* Salt is easily extensible (not by forking the project), but in
  your own environment by simply putting the module for your backend of choice
  under a specific path.

  Or, to put this differently, if you need a different backend, or an additional
  feature, you won't need to fork the entire project and re-compile it; instead,
  you can preserve the existing usage and just provide it with your own code
  implementing the feature or backend you need.

Installation
------------

```bash
$ pip install salt-confd
```
