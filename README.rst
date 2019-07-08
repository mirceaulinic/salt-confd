salt-confd
----------

Lightweight Salt package for `confd 
<https://github.com/kelseyhightower/confd>`__ style management of local
application configuration files.

Why
~~~

Please note that the intent of this software package is not to compete against
``confd`` or other popular equivalents; it was born purely out of my personal
preference / bias of using Salt for managing files (and others). Salt is
typically at the opposite end of "lightweight" and this package aims to
alleviate this, however it still cannot get better than confd - from this
perspective. Alas, it's written in Python.

If you want, in short, here's why I took this approach:

1. Why not?
2. It's fun.
3. I like Salt, and it offers a variety of well-known templating languages to
   manage the files, including Jinja, Mako, Cheetah, or even pure Python - and
   others.
4. What I find missing in confd is the possibility to manage the local config
   files based on more environment parameters - e.g., have idempotent templates
   that can be used across a number of distributions (as in opposite to having
   separate files / directory tree / or even repositories for different
   base operating system distribution); with Salt, this can be very easily done
   using the Grains.
5. It's a common practice to provide an alternative to an existing software, in
   another widely used programming language.
6. Salt covers a large variety of backends to fetch the data from (including 
   Redis, Consul, etcd, and so on).

   Additionally, Salt is easily extensible (not by forking the project), but in
   your own environment by simply putting the module for your backend of choice
   under a specific path.

Installation
~~~~~~~~~~~~

.. code-block:: bash

    $ pip install salt-confd
