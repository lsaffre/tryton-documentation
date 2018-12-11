Migration
=========

The migration between tryton versions is fully supported. In order to migrate
an existing database to a newer version you must take the following actions:

1. Obtain the new version of trytond and all the instaled modules. You can
   update your existing installation or create a new one.
2. Update the database with `trytond -u all -d <database>`, where `<database>`
   refers to your database name.


Migrating custom modules
------------------------

If you have developed custom modules it's possible that you have to adapt
your code in order to get it working with the new tryton version.

Normally, there is an entry on the wiki_ with the changes that must be done and
an example of the change in one official module. You can find this entries under
the `Release process`_ entry.

.. _wiki : http://code.google.com/p/tryton/wiki
.. _Release process : http://code.google.com/p/tryton/wiki/ReleaseGeneral
