Paramiko presentation examples
==============================

Why hello, there. If you are reading this, chances are you listened to my
presentation on the paramiko Python library on 2022-06-14. This repo contains
some examples.

Pre-requisites
--------------

In order to try the scripts out, all you need is:

* Python 3.4 or above (recommended: Python 3.10)

* An SSH server you can access (if you're using a modern Linux distribution,
  it should be part of your distribution).

* An SSH client (by default, this should be installed)

The Python requirements are listed in the `requirements.txt`, which you can
install the following ways:

* System-wide:

  .. code:: shell

     # python3 -m pip install -r requirements.txt

* User-level:

  .. code:: shell

     $ python3 -m pip install --user -r requirements.txt

Contents
--------

* **simple-command.py** - Execute the given command on the SSH server.

* **host-keys.py** - Example that demonstrates host key handling

* **copy-from-host.py** and **copy-to-host.py** - SFtp file transfer example

* **list-files.py** - SFtp list files in directory exampke

* **greeting-server.py** - Server example that greets you when you log in

* **honeypot-server.py** - Server that accepts all password logins and does nothing

* **echo-subsystem.py** - Simple echo server demonstrating SSH subsystems

Note for help
.............

Each script has a `--help` option in case the parameters aren't apparent. This is the
only documentation for the example scripts.
