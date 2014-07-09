Installation Procedure
======================

Tryton is separated into independent parts:

- the server named ``trytond``
- the GTK client named ``tryton``
- and several modules to extends server capabilities (ie: account, bank, party, project...)


Installing from PyPI
--------------------

You can directly install all these independentely using pip command-line tool
on your system (or in a virtualenv, a recommended setup) as each of these are
available on the Python Package Index. Here's how to proceed:

- Installing the server

  .. code-block:: bash

      pip install trytond

- Installing the GTK client

  .. code-block:: bash

      pip install tryton

- Installing any module for server:

  .. code-block:: bash

      pip install trytond_MODULE_NAME    # Replace MODULE_NAME with the name of the module

  You might be interested by a `list of available modules
  <https://pypi.python.org/pypi?:action=browse&show=all&c=551>`_.


.. note::

    Refer to `Virtualenv Docs <https://pypi.python.org/pypi/virtualenv/>`_ for
    getting started with virtualenv. A recommend way to get your tryton application
    and it's dependency separated from your system libraries. Although `virtualenv`
    is not required, you should think about using it.


Installing from system packages
-------------------------------

Specific packages are available for Windows, MacOSX, various
Linux flavor, and BSD. These can be find on the `Tryton Download Page
<http://www.tryton.org/download.html>`_.

Valuable information specific to each system can be found on
the `tryton wiki <https://code.google.com/p/tryton/wiki/InstallationOS>`_.


Installing from source
----------------------

For developer, you can browse the `Source Code Repository <http://hg.tryton.org/>` and
download source code thanks to your favorite version control system:

- Get server source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/trytond/   # For the server


- Get GTK client source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/tryton/    # For the client


- Get official modules source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/modules/MODULE_NAME

  You might be interested by a list of `actual module repositories <http://hg.tryton.org/modules>`.

And up-to-date, but non-official git repositories are maintained on github:

  .. code-block:: bash

      git clone https://github.com/tryton/tryton.git
      git clone https://github.com/tryton/trytond.git
      git clone https://github.com/tryton/MODULE_NAME.git

If using ``tar.gz`` or getting source by version controlled repository, don't forget to
install each package with this command-line (to be run in the root of the package):

  .. code-block:: bash

      python setup.py install

.. note::

  Using virtualenv is encouraged, especially if you want to develop or if tryton
  packages are installed on a system along with other important, unrelated services.
  Refer to `Virtualenv Docs <https://pypi.python.org/pypi/virtualenv/>`_ for
  getting started with virtualenv.


Preparing Application Servers
-----------------------------

TODO


Basic Database Configuration
----------------------------

Postgres is the recommended database engine for tryton
Install Postgres database. Steps for installing Postgres can be
found from `Postgres Installation <http://wiki.postgresql.org/wiki/Detailed_installation_guides/>`_
Install the database and give a new password to the postgres database
user.


Creating a Virtualenv
`````````````````````

Refer to `Virtualenv Docs <https://pypi.python.org/pypi/virtualenv/>`_
for getting started with virtualenv.

Create the virtualenv and activate the virtualenv you created.

.. code-block:: bash

    $ sudo easy_install virtualenv  # to install virtualenv
    $ virtualenv foobar             # to create a virtualenv
    $ source foobar/bin/activate    # to activate the virtualenv
    $ deactivate                    # to deactivate the virtualenv

Now you can install ``tryton`` and ``trytond`` in your virtualenv by using pip
commands.
