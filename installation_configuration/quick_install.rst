Quick install guide
===================

Before you can start using Tryton, you'll need to get it installed. We
have a :doc:`detailed installation guide <installation>` that covers all
the possibilities; this guide will guide you to a simple, minimal
installation that'll work while you explore, test or evaluate tryton.

Components
----------

Tryton is separated into three different parts:

1. The tryton server named ``trytond`` (d for `daemon <https://en.wikipedia.org/wiki/Daemon_(computing)>`_)
2. The tryton desktop client.
3. The modules that extend or implement features on server (like inventory 
   management, sales management, accounting, invoicing etc.)


Neso
----

Neso is a standalone suite which includes the server, client and modules
and uses a light weight database called SQLite_. Neso is a great way to
explore tryton and using Tryton for a single user.

You could download the `installer for windows <http://downloads.tryton.org/3.2/neso-setup-3.2.1.exe>`_
or install it from source.

.. _SQLite: https://en.wikipedia.org/wiki/Sqlite

Install Python
--------------

Being a python based system, Tryton requires Python to run. Tryton works
with Python 2.7. Python 2.7 also includes a light weight database called
SQLite so you won't need to set up a database just yet.

You can verify that Python is installed by typing ``python`` from your
shell; you should see something like::

    Python 2.7.5 (default, Oct  8 2013, 17:30:18)
    [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.2.75)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Setup a database
----------------

This step is only necessary if you would like to work with a more powerful
database engine like PostgreSQL or MySQL. To install such a database
consult the :ref:`database-configuration` section.
If all you want is to get started quickly on tryton and use SQLite as a database,
add the following to your trytond.conf (normally /etc/trytond.conf)::

    db_type = sqlite
    data_path = /var/lib/trytond

and make sure data_path is an existing directory

Install Tryton
--------------

You've got three easy options to install Tryton:

* Install a version of Tryton provided by your 
  :ref:`operating system distribution <install-from-system-distributions>`.
  This is the quickest option for those who have operating systems that 
  distribute Tryton.
* :ref:`Install an official release <install-official-release>`. This is the
  best approach for users who want a stable version number and aren’t concerned
  about running a slightly older version of Tryton.
* :ref:`Install the latest development version <install-the-development-version>`. 
  This is best for users who want the latest-and-greatest features and aren’t
  afraid of running brand-new code.


Verifying
---------

To verify that Tryton is installed, type ``trytond --version`` from your
shell; you should see something like::

    trytond 3.2.1

This indicates the version of Tryton installed.
