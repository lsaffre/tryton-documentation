Installation Procedure
======================

Tryton is separated into independent parts:

- the server named ``trytond``
- the GTK client named ``tryton``
- and several modules to extends server capabilities (ie: account, bank, party, project...)

Installation instructions are slightly different depending on whether you’re
installing a distribution-specific package, downloading the latest official
release, or fetching the latest development version.

It’s easy, no matter which way you choose.

.. _install-from-system-distributions:

Installing from system distributions
------------------------------------

Many third-party distributors are now providing versions of Tryton
integrated with their package-management systems. These can make
installation and upgrading much easier for users of Tryton since the
integration includes the ability to automatically install dependencies
(like database adapters) that Tryton requires.

If you’re using Linux or a Unix installation, such as Ubuntu, check with
your package manager if they already package Tryton. The Tryton Wiki also
contains instructions for 
`installation on several distributions <https://code.google.com/p/tryton/wiki/InstallationOS>`_.

Specific packages are available for Windows and MacOSX, which can be downloaded
from the `tryton download page <http://www.tryton.org/download.html>`_.

.. tip::

    While most packages are based on the latest stable versions of Tryton, if
    the version you need is not available, you'll need to follow the
    instructions for :ref:`installing an official release <install-official-release>`
    or :ref:`development versions <install-the-development-version>`.


.. _install-official-release:


Installing an official release with ``pip``
-------------------------------------------

This is the recommended way to install Tryton. The packages are downloaded
automatically from the Python package index (PYPI).

1. Install pip_. The easiest is to use the `standalone pip installer`_. If your
   distribution already has ``pip`` installed, you might need to update it if
   it's outdated. (If it's outdated, you'll know because installation won't
   work.)

2. (optional but recommended) Take a look at virtualenv_ and virtualenvwrapper_. 
   These tools provide isolated Python environments, which are more practical than
   installing packages systemwide. They also allow installing packages
   without administrator privileges. It's up to you to decide if you want to
   learn and use them.

3. If you're using Linux, Mac OS X or some other flavor of Unix, enter the
   command ``sudo pip install trytond`` at the shell prompt. If you're using
   Windows, start a command shell with administrator privileges and run
   the command ``pip install trytond``. This will install Tryton server in 
   your Python installation's ``site-packages`` directory.

   Similarly, you can install the Tryton client with the command ``pip
   install tryton`` and modules with ``pip install trytond_MODULE_NAME``

.. tip::

   If you're using a virtualenv, you don't need ``sudo`` or administrator
   privileges, and this will install Tryton in the virtualenv's
   ``site-packages`` directory.

.. tip::

   You might be interested by a `list of available modules 
   <https://pypi.python.org/pypi?:action=browse&show=all&c=551>`_.


.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/en/latest/
.. _standalone pip installer: http://www.pip-installer.org/en/latest/installing.html#using-the-installer


Useful pip command combinations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Ensure that PIP is the latest version: 

  .. code-block:: bash

      pip install -U pip

- Installing the server

  .. code-block:: bash

      pip install trytond

- Installing the GTK client

  .. code-block:: bash

      pip install tryton

- Installing any module for server
      
  .. code-block:: bash

      pip install trytond_MODULE_NAME

  Replace MODULE_NAME with the name of the module. Example below.

  .. code-block:: bash


      pip install trytond_sale
   
  remember that it installs the most recent released version, as of this
  writing that is the 3.2 series.


- Installing the most recent version from a previous series:

  .. code-block:: bash

      pip install "trytond_sale>=3.0,<3.1"
   
  Installs latest version in the 3.0 series

- Upgrading a module

  .. code-block:: bash

      pip install -U trytond_sale
   
   remember that this would install the most recent series which as of this
   writing is 3.2

- Upgrading within the same series

  .. code-block:: bash

      pip install -U "trytond_sale>=3.0,<3.1"

- Upgrade only the module, without any dependencies

  .. code-block:: bash

      pip install -U --no-deps "trytond_sale>=3.0,<3.1"
   
- Installing a module from source code

  .. code-block:: bash

      pip install /path/to/module/folder

- Forcefully reinstall a module

  .. code-block:: bash

      pip install -U --force trytond_sale


Installing an official release manually
---------------------------------------

1. Download the latest release from our `download page`_.

2. Untar the downloaded file (e.g. ``tar xzvf trytond-X.Y.Z.tar.gz``,
   where ``X.Y.Z`` is the version number of the release).
   If you're using Windows, you can download the command-line tool
   bsdtar_ to do this, or you can use a GUI-based tool such as 7-zip_.

3. Change into the directory created in step 2 (e.g. ``cd trytond-X.Y.Z``).

4. If you're using Linux, Mac OS X or some other flavor of Unix, enter the
   command ``sudo python setup.py install`` at the shell prompt. If you're
   using Windows, start a command shell with administrator privileges and
   run the command ``python setup.py install``. This will install Trytond in
   your Python installation's ``site-packages`` directory.

   .. admonition:: Removing an old version

       If you use this installation technique, it is particularly important
       that you remove old versions of Tryton. TODO: explain how

.. _download page: http://www.tryton.org/download.html
.. _bsdtar: http://gnuwin32.sourceforge.net/packages/bsdtar.htm
.. _7-zip: http://www.7-zip.org/

.. _install-the-development-version:

Installing from source
----------------------

You can browse the `Source Code Repository <http://hg.tryton.org/>` and
download source code thanks to your favorite version control system:

1. Make sure that you have Git_ or Hg_ installed and that you can run its
   commands from a shell. (Enter `git help` or `hg help` to test this).

2. Checkout the development branch of the source code from the VCS (See
   examples below).

3. Make sure that the Python interpreter can load the downloaded code. The
   most convenient way to do this is via pip_. Run the following command:

   .. code-block:: bash

      sudo pip install -e trytond-trunk/

  (If using a virtualenv_ you can omit ``sudo``.)
 
.. warning::

    Don't run ``sudo python setup.py install``, because you've already
    carried out the equivalent actions in step 3.

Official mercurial repos
~~~~~~~~~~~~~~~~~~~~~~~~

- Get server source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/trytond/ trytond-trunk  # For the server


- Get GTK client source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/tryton/ tryton-trunk   # For the client


- Get official modules source code

  .. code-block:: bash

      hg clone http://hg.tryton.org/modules/MODULE_NAME MODULE_NAME-trunk

  You might be interested by a list of `actual module repositories <http://hg.tryton.org/modules>`.

When you want to update your copy of the Tryton source code, just run the
command ``hg pull -U`` from within the corresponding directory. When you do
this, Mercurial will automatically download any changes.

Unofficial Git mirror
~~~~~~~~~~~~~~~~~~~~~

And up-to-date, but non-official git repositories are maintained on github:

- Get server source code

  .. code-block:: bash

      git clone https://github.com/tryton/trytond.git trytond-trunk

- Get GTK client source code

  .. code-block:: bash      

      git clone https://github.com/tryton/tryton.git tryton-trunk

- Get official modules source code

  .. code-block:: bash


      git clone https://github.com/tryton/MODULE_NAME.git MODULE_NAME-trunk

When you want to update your copy of the Tryton source code, just run the
command ``git pull`` from within the corresponding directory. When you do
this, Git will automatically download any changes.


.. _Git: http://git-scm.com/
.. _Hg: http://mercurial.selenic.com/

Preparing Application Servers
-----------------------------

TODO

.. _database-configuration:

Basic Database Configuration
----------------------------

Postgres is the recommended database engine for tryton
Install Postgres database. Steps for installing Postgres can be
found from `Postgres Installation <http://wiki.postgresql.org/wiki/Detailed_installation_guides/>`_
Install the database and give a new password to the postgres database
user.
