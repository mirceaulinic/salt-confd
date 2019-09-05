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

I see it rather as a trade-off: while ``confd`` is only a 5MB binary, I haven't
managed yet to have this installation (together with dependencies) under 76MB.
That said, if you already have Salt installed, you might find this helpful, as
all you've got to do is install this package, which in this case would bring a
tiny overhead. Otherwise, I'd invite you to evaluate: with ``salt-confd`` you
can do a lot more than the original ``confd`` (see also some notes and examples
below), though the decision if yours to balance your requirements and goals vs.
the additional overhead.

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
* For monitoring/logging purposes, you might want to send the results somewhere,
  or simply have some post-checks / validate the output.

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

You can display the previous return as JSON, which could be helpful in
combination with ``jq`` to validate the output, e.g.,

```bash
$ salt-confd --out=json
{
    "local": {
        "file_|-/tmp/test_|-/tmp/test_|-managed": {
            "changes": {
                "diff": "--- \n+++ \n@@ -0,0 +1,7 @@\n+Hello world!\n+\n+I'm running on Ubuntu 18.04, and I have the\n+following IPv6 addresses:\n+- ::1\n+- fe80::42:57ff:fe55:2afc\n+- fe80::9a9:9f9e:9a2c:6bf1\n"
            },
            "pchanges": {},
            "comment": "File /tmp/test updated",
            "name": "/tmp/test",
            "result": true,
            "__sls__": "confd",
            "__run_num__": 0,
            "start_time": "13:17:12.342262",
            "duration": 26.274,
            "__id__": "/tmp/test"
        }
    }
}
```

Additionally, if you'd like to log in a Slack (or other places) the changes
salt-confd is applying, you can execute with:

```bash
$ salt-confd --return slack
```

After setting the details into the configuration file (by default
``/etc/salt/confd.yml``), as 
[documented](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.slack_returner.html),
e.g.,

``/etc/salt/confd.yml``

```yaml
slack.channel: salt-confd
slack.api_key: <api key>
slack.username: salt-confd
slack.as_user: salt-confd
slack.yaml_format: true
```

To always send the output to Slack or where you'd like to monitor these changes,
add the following line to ``/etc/salt/confd.yml``:

```yaml
returner: slack
```

In brief, there are 3 steps to follow:

1. Install ``salt-confd``.
2. Put the files as mentioned above (i.e., as you'd do when using the original
   ``confd``).
3. Run ``salt-confd``.

What is this thing
------------------

This plugin is simply a wrapper executing various Salt internal code, with
bespoken configuration options and customised calls, in such a way to facilitate
the management of the configuration files to provide a more straight forward
experience.
