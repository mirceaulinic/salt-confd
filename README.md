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
* Not only local templates: it often happens to have your template on a server
  elsewhere; at the end of the day, you need the resulting config file, not its
  source.
  With Salt Confd, you can use source files directly available via HTTP, S3,
  SWIFT, SVN, or FTP.
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

Usage
-----

In the spirit of the original confd, I tried to preserve the CLI syntax and the
general usage. Under the ``confdir`` directory (defaulting to
``/etc/salt/confd``), you'd need to have the following structure:

```bash
$ tree /etc/salt/confd
.
|-- conf.d/
|   `-- test.sls
`-- templates/
    `-- test.conf
```

That is, a subdirectory named ``conf.d`` having one or more files. The file
extension doesn't matter, as the content is going to be interpreted as SLS, by
default rendered as Jinja + YAML. This format could be however changed, by
adding a hashbang at the top of the file, as detailed in [this 
document](https://docs.saltstack.com/en/latest/ref/renderers/#overriding-the-default-renderer).

For example, the contents of the ``test.sls`` file above:

```yaml
src: test.conf
dest: /tmp/test
```

Where ``test.conf`` is the template file from the ``templates/`` directory:

```jinja
Hello world!

I'm running on {{ grains.osfullname }} {{ grains.osrelease }}, and I have the
following IPv6 addresses:

{%- for addr in grains.ipv6 %}
- {{ addr }}
{%- endfor %}
```

With these two simple files, running ``salt-confd``:

```bash
$ salt-confd
local:
----------
          ID: /tmp/test
    Function: file.managed
      Result: True
     Comment: File /tmp/test updated
     Started: 12:20:54.781405
    Duration: 26.337 ms
     Changes:   
              ----------
              diff:
                  --- 
                  +++ 
                  @@ -0,0 +1,7 @@
                  +Hello world!
                  +
                  +I'm running on Ubuntu 18.04, and I have the
                  +following IPv6 addresses:
                  +- ::1
                  +- fe80::42:57ff:fe55:2afc
                  +- fe80::9a9:9f9e:9a2c:6bf1

Summary for local
------------
Succeeded: 1 (changed=1)
Failed:    0
------------
Total states run:     1
Total run time:  26.337 ms
```

In brief, there are 3 steps to follow:

1. Install ``salt-confd``.
2. Put the files as mentioned above (i.e., as you'd do when using the original
   ``confd``).
3. Run ``salt-confd``.
