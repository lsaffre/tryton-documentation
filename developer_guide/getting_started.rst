Getting Started
===============


Setting up a development environment
------------------------------------
In the previous chapter you have seen how to install tryton client on your
machine. Now, lets start with setting up the development environment for
tryton.

Steps for setting up a development environment for tryton.

1. First thing is to have Python2 running on your system.
   You can check if python is installed by typing **python2** in a console window
   and pressing **Enter**.
   If python is not installed, consult your package manager for your operating system.  
   Or go to www.python.org and select "Downloads"
   If python is installed an interactive shell will open, printing out version info
   and **>>>**
   You can exit by calling the function **exit()** or by pressing **ctrl+d**

2. Next, Install Posgres database. Steps for installing Postgres can be
   found from `Postgres Installation <http://wiki.postgresql.org/wiki/Detailed_installation_guides/>`_
   Install the database and give the database user postgres a new
   password.

3. Set up the virtual environment and install tryton client and trytond.
   You can directly install Tryton using pip command-line tool in your
   virtualev.

    .. code-block:: bash

        $ pip install trytond
        $ pip install tryton_module_name

    Replace module_name with the name of the module you want to install


Using HgNested
~~~~~~~~~~~~~~

`HgNested <http://code.google.com/p/hgnested/>`_ is a mercuarial extension
used to work on nested repositories. In order to install hgnested you must run:

::

  pip install hgnested

Once installed you can checkout the lastest sources by executing:

::

  hg nclone http://hg.tryton.org/trytond

This will also clone all the modules in trytond/modules.

In order to run the tryton server you must install all the requirements as
described on the `Wiki <http://code.google.com/p/tryton/wiki/Requirements#Requirements_for_the_Tryton_Server>`_.

After this you can run your server with:

::

  trytond/bin/trytond

Using virtualenvwrappers templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Openlabs guys have created a virtualenvwrapper template to get a virtualenv
created with all the required dependencies (except your database drivers).

You can install it executing:

::

  pip install virtualenvwrapper.tryton

You can create a virtualenv with the latest version of tryton running:

::

  mkproject -t tryton virtualenv_name

In the virtualenv you can run your tryton server by executing:

::

  trytond


For more information about available templates please refer to
`virtualenvwrapper.tryton repository <https://github.com/openlabs/virtualenvwrapper.tryton>`_


