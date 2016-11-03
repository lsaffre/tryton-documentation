Tryton by example: library
==========================

Almost every Tryton functionality that you are going to develop on a daily
basis is enclosed into the modules. In order to get an idea of available
modules you should take a look inside trytond/modules. You will see many
folders in the modules. Each one comprises one set of facilities that can
be installed and will be available to the end users. Some examples are
company, country, currency and party.

Module structure
----------------

First thing in the birth of a new module is the creation of a python package
with the following structure::

    /library
        /tryton.cfg
        /__init__.py
        /library.py
        /library.xml
        /view
            /book_form.xml
            /book_tree.xml

Let's see the contents and purpose of each one in detail:

tryton.cfg
~~~~~~~~~~

This file must be present at the root of your module's directory. It contains
the server-version the module was developed for, a list of the xml files the module contains
and the modules it depends on:

::

    [tryton]
    version=3.2.1
    depends:
        ir
    xml:
        library.xml

In this case we are creating a module for trytond 3.2 series.
We state that library.xml has to be parsed and our module doesn't have any real dependencies
(ir is a builtin module)

library.xml
~~~~~~~~~~~

All our static data is usually put into xml files.
    * actions
    * views
    * reports
    * users/groups
    * access restrictions

Observe that this file is a *regular* xml file. So it starts with the ordinary
xml version declaration at the top, and it has as its master element the
*tryton* element, followed by a *data* element. The other elements will all be
children of *data*

.. code-block:: xml
   :linenos:

    <?xml version="1.0"?>
    <tryton>
        <data>
            <!-- All our definitions come here -->
        </data>
    </tryton>


\__init__.py
~~~~~~~~~~~~

This file must be present at the root of your module's directory. It serves
two main purposes: it transforms your directory into a Python visible package
(according to Python general rules) and it also registers in the
:py:class:`~trytond.pool.Pool` the entity classes of the module.

You can think of the Pool as a "in memory synchronized image" of
your database, because Tryton follows the so called
`active record pattern <http://en.wikipedia.org/wiki/Active_record_pattern>`_.
Tryton takes care of database table creation and of the mapping between the
in-memory representation of the entity and the respective columns in the
database. It also takes care of the synchronization of the data loaded in your
in-memory entities and the persistent data on the database.

Whenever we are building a module in Tryton, we deal with a high-level,
object-oriented representation of our entities. Generally, we are free from
writing explicit SQL or python-sql instructions, but in order for this *magic*
to happen, Tryton's Pool must be "aware" of the
existence of your entity classes.

.. code-block:: python

    from trytond.pool import Pool
    from .library import Book

    def register():
        Pool.register(
            Book,
            module='library', type_='model'
        )

In the example above, we are registering the *Book* class into the *Pool*.
Whenever the trytond service runs, it starts with initializing every module
that is installed (more on that in the coming lines), i.e., it performs the
regular Python initialization of packages. That means the execution of the
code contained inside the __init__.py.

If you are unfamiliar with the package initialization, you can think of it as
performing an analogous role as the __init__ method inside a Python class,
but, in this case, it performs initialization tasks semantically relative to
the whole package.

library.py
~~~~~~~~~~

This file must be present at the root of your module's directory. According to
a domain model, it contains the entity classes.


If your domain model is a commercial enterprise, your domain model would
contain entities such as *SaleOrder*, *Product*, *Customer* and so on. Our
tutorial here is proposing a library domain model, where you would expect to
find *Book*, *Author*, *Publisher*, etc. A domain model encompasses real world
objects that your software solution is expected to deal with.

In our tutorial, we are going to have a simple Book model. It has some fields
associated with it: *title*, *isbn*, *subject*, *abstract*.

Each field has a **Type**. This type determines many aspects and behaviours
of the application. For instance,

* :py:class:`~trytond.model.fields.Char` field will be created as a
  *Char Varying* column inside the database.
* :py:class:`~trytond.model.fields.Text` field will be displayed as a large
  text box in the Tryton Client window and so on.

In order to know every field avaliable, you can consult official Trytond
docs: :py:mod:`~trytond.model.fields`

Defining the model
------------------

.. code-block:: python

    from trytond.model import ModelView, ModelSQL, fields

    # list of all classes in the file
    __all__ = ['Book']


    class Book(ModelSQL, ModelView):
        # description (mandatory on first declaration)
        'Book'

        # Internal class name. Always used as a reference inside Tryton
        # default: '<module_name>.<class_name>' on Tryton
        # becomes '<module_name>_<class_name>' in the database
        __name__ = 'library.book'

        title = fields.Char('Title', required=True)
        isbn = fields.Char('ISBN')
        subject = fields.Char('Subject')
        abstract = fields.Text('Abstract')

In our example we have defined four fields in the class. Tryton will
automatically create a table in the database called **library_book**,
consisting of **nine** columns: the four defined above and another five that
are present on every column of the database:

* id
* create_date
* write_date
* create_uid
* write_uid

The first column is the **surrogate primary key** of the table. The following
ones are self-explanatory, and are created for auditing purposes. In general,
we should not worry about those columns, because Tryton takes care of them for us.

If you access the defined database, you are going to see the the aforementioned
table created.


Creating the View
-----------------

As we need our model to appear in the client we have to define a view.
A complete list of all the available views can be found in
:ref:`Tryton docs <trytond:topics-views>`, but in this tutorial we're only
going to define the following for our module:

    * tree view: to display a list of all our books
    * form view: to view and modify all the details of one single book at a time

Each view is defined by its own xml-file which has to be placed in the 'view' folder
of the module.
Again this is a regular xml file with the following structure:

.. code-block:: xml
   :linenos:

    <?xml version="1.0"?>
    <!-- This file is part of Tryton.  The COPYRIGHT file at the top level of
    this repository contains the full copyright notices and license terms. -->
    <form string="Books" col="6">
        <label name="title"/>
        <field name="title" colspan="3"/>
        <label name="isbn"/>
        <field name="isbn"/>
    </form>

in our simple case we only need labels to put a translated version of our field name and fields
to input/view field-data. There is a lot more formatting tags available which can be looked up from
:ref:`Tryton docs <trytond:topics-views>`


adding a menu
~~~~~~~~~~~~~

In order to create a new menu we have to edit the library.xml file so it will
contain the declaration of our menu and its respective menu item (submenu):

.. code-block:: xml
   :linenos:

    <menuitem name="Library" sequence="0" id="menu_library"/>
    <menuitem name="Books" parent="menu_library" id="menu_books" action="act_library_window"/>


In the xml file above we have declared two *menuitems*. The first one, named
*Library* will be placed on the root menu of Tryton client. Observe that it
has, besides the name attribute, a sequence, that indicates the position of the
menu, and an id, that must be **unique**. This id will identify this element
to the rest of the software. It will be placed on the root menu because it has
no parents.

The second *menuitem*, named *Books* has another element: a *parent* element,
which points to the id of the former menu (*id="menu_library"*), indicating
that it is going to be nested on the first one. this menu-item also has an associated
action to call: 'act_library_window'.

Associating the views
~~~~~~~~~~~~~~~~~~~~~

there is four types of actions we could call from our menu-entry:

    * ir.action.act_window
    * ir.action.report
    * ir.action.wizard
    * ir.action.url

obviously we want to use act_window, which should open up a new tab in the client:

.. code-block:: xml
   :linenos:

    <record model="ir.action.act_window" id="act_library_window">
        <field name="name">Books</field>
        <field name="res_model">library.book</field>
    </record>

.. note:: Our action has to be defined **before** referencing in the menu

We can then add different window-views to our newly created window:

.. code-block:: xml
   :linenos:

    <record model="ir.action.act_window.view" id="act_library_view1">
        <field name="sequence" eval="10"/>
        <field name="view" ref="library_view_tree"/>
        <field name="act_window" ref="act_library_window"/>
    </record>

which themselves point to views

.. code-block:: xml
   :linenos:

    <record model="ir.ui.view" id="library_view_tree">
        <field name="model">library.book</field>
        <field name="type">tree</field>
        <field name="name">book_tree</field>
    </record>

Where the "name" field points to our xml-file (form/book_tree.xml) containing the actual layout
of the view.

Installing the package
----------------------

When installing your package you can either link directly in the modules folder of tryton or
use python setuptools (recommended).
to use python-setuptools:

- obtain the
  `contrib-module-setup.tmpl <http://hg.tryton.org/tryton-tools/file/b1bf3e9fe771/contrib-module-setup.tmpl>`_
  from hg.tryton.org/tryton-tools
- replace 'MODULE' and 'PREFIX' with your desired values
- save the file in your module-root as 'setup.py'
- install like any other module (refer to the :ref:`installation guide <install-the-development-version>`)


Applying changes
----------------

In order for your changes to be applied we need to insert the module in the
database.
You can either achieve this by installing the module within the client or directly from
command line using -i (insert)::

    TRYTOND_HOME/trytond/bin/trytond -d NAME_OF_THE_DATABASE -i MODULE_NAME

Whenever you make changes to the module, those changes can be applied by
using the -u flag (update)::

    TRYTOND_HOME/trytond/bin/trytond -d NAME_OF_THE_DATABASE -u MODULE_NAME

Let's also restart the Tryton client now. Remember to start it with the **-d**
(development) flag, so it can update the cache and show the changes we have
just made:

.. code-block:: bash

    TRYTON_HOME/tryton/bin/tryton -d

When you log in again on the client, you are going to see that the menu
*Library* and the submenu *Books* have been created.


