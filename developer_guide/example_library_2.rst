Tryton by example (2): library_rent
===================================

Now that we have created a working library-module which gives us the possibility to store
information about all our books, we might find ourselves in a situation where we want
to rent those books out and keep track of our friends who currently hold them.
Because we read our books from time to time we also want to know if its currently available
or not.

Field functions
---------------

As we already learned about trytons inheritance-model from :ref:`basic concepts<model-inheritance>`,
we create a new module folder called 'library_rent' in the same structure as
the one from last chapter, and we include 'library' as its dependency in tryton.cfg.
We start by adding a simple :py:class:`~trytond.model.fields.char`
field straight away (we don't know any better yet):

.. code-block:: python

    class Book:
        __name__ = 'library.book'
        renter = fields.Char('Rented by')

Next thing is to find out if the book is available or not, but we don't want to manually set the
state each time we rent out a book.
Tryton has some handy field-functions to offer so we can automate this task.

.. note::

    Field-functions are always executed on the server, but they may also be triggered from the client.


Field-Relationships
^^^^^^^^^^^^^^^^^^^

If you have a pair of fields that influence each others value, you can define functions to update
the fields values whenever a change is detected.
There is two use-cases for this:

Updating a field should trigger an update on a number of fields
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    * define a function named on_change_<field_name>
    * return a dictionary containing {'field_name': value} for all fields to be updated
    * decorate the function with @fields.depends(\*keys) containing all keys to be updated or required
      for calculation.
      this ensures that all the fields get submitted by the client.


.. code-block:: python

    class Book:
        available = fields.Boolean('Available for rent')

        @fields.depends('available')
        def on_change_renter(self):
            if self.renter:
                return {'available': False}
            else:
                return {'available': True}


Updating a set of fields should trigger an update on a single field
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    * define a function named on_change_with_<field_B_name>
    * return the fields new value
    * decorate the function with @fields.depends(\*keys) using all the keys that may influence the field

.. code-block:: python

    class Book:
        available = fields.Boolean('Available for rent')

        @fields.depends('renter')
        def on_change_with_available(self):
            return self.renter == ''

.. note:: on_change_* and on_change_with_* are called from the client

Function fields
^^^^^^^^^^^^^^^

The previous 'on_change_owner' example could have been solved without storing a new key
in the database by calculating its value on the fly.
To achieve this we need to add a function field:

.. code-block:: python

    class Book:
        available = fields.Function(fields.Boolean('Available'), 'get_renter_information')

        def get_renter_information(self, name):
            return self.renter == ''

where name is the fields name.
This special field can be accessed just as if it was a normal field
of the type specified but gets computed each time (on the server)

.. note:: function fields are calculated on the server and may be incorrect when a value is changed in the client

Combining on_change with a Function field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we know about those concepts we can even have all the advantages of Function fields
(no extra database-column) and on_change_* functions (updated in the client) by combining them:

.. code-block:: python

    class Book:
        available = fields.Function(fields.Boolean('Available for rent'), 'on_change_with_available')

        @fields.depends('renter')
        def on_change_with_available(self, name=None):
            return self.renter == ''

So we have that problem solved.

Default values
^^^^^^^^^^^^^^

After a while, we recognize that whenever there is a new book in our library, we want to read it first.
We don't want to rent it out by accident, so by default we should be the renter on a new library-entry.

You can define default values for fields by adding a 'default_<field_name>' function to your model:

.. code-block:: python

    class Book:
        __name__ = 'library.book'
        renter = fields.Char('Rented by')

        def default_renter():
            return 'me'

Relational Fields
-----------------

It turns out that actually there is a lot more than just a hand of forename-friends who want to rent
our books, so we want to store a bit of additional information with our renters.
We have a good run and find out that tryton already has a useful
`Party Module <http://doc.tryton.org/3.2/modules/party/doc/index.html>`_ to offer,
so all we have to do is to extend our book model by a new field to reference a party who currently
rents the book from our library.

Like any `ORM <http://en.wikipedia.org/wiki/Object-relational_mapping>`_ Tryton offers relational fields,
which enable you to connect model(s) to its related model(s). You can use any of these:

    - Many2Many - for example (Many) models can belong to a category but also to other (Many) categories
    - Many2One - Connect a set of (Many) models to a parent (One) (example: a company field in company.employee Model)
    - One2Many - A field representing (Many) connected model instances (example employees field in company.company model)
    - One2One

Given that information, we could solve our Library example a bit more elegant by using Trytons built-in Party model
and rent books only to registered parties:

.. code-block:: python

    class Book:
        __name__ = 'library.book'
        renter = fields.Many2One('party.party', 'Renter', required=False)

    class User:
        __name__ = 'party.party'
        rented_books = fields.One2Many('library.book', 'renter', 'Rented Books')

.. note:: The One2Many field requires a Many2One field to be referred in the related Model.

Transactions
------------

TODO


Creating Reports
----------------
Add the following line to the file 'library.xml' into the /data tag :

.. code-block:: xml

        <!-- First thing: define the report itself,
        model: Target-Model
        report_name: the report class' __name__
        report: template ods-file
        -->
        <record model="ir.action.report" id="report_library">
            <field name="name">Book</field>
            <field name="model">library.book</field>
            <field name="report_name">library.book</field>
            <field name="report">library/book.odt</field>
        </record>
        <!-- Second we register a keyword
        (so we can call the report from tryton client) -->
        <record model="ir.action.keyword" id="report_library_book">
            <field name="keyword">form_print</field>
            <field name="model">library.book,-1</field>
            <field name="action" ref="report_library"/>
        </record>

Now create the file book.odt inside your module.
In this file add the following lines by adding a placeholder in your odt
file.

.. code-block:: xml

   <for each="library in objects">
   <library.title>
   </for>

.. tip::

    placeholders can be inserted in libreoffice by pressing **ctrl+f2**
    **functions -> placeholder -> text**

In case you are dealing with ods file. For adding a placeholder you have
to add a hyperlink.


Wizard
------

A wizard is a fine state machine.

:py:class:`~trytond.wizard.Wizard(session_id)`
This is the base for any wizard. It contains the engine for the finite
state machine. A wizard must have some state instance attributes that the
engine will use.


Class attributes are:
**Wizard.__name__**
It contains the unique name to reference the wizard throughout the platform.


**Wizard.start_state**
   It contains the name of the starting state.

**Wizard.end_state**
   It contains the name of the ending state.

**Wizard.__rpc__**
   Same as trytond.model.Model.__rpc__.

**Wizard.states**
   It contains a dictionary with state name as key and State as value


.. code-block:: python

   from trytond.wizard import Wizard, StateView, StateTransition, Button

   class PrintLibraryReportStart(ModelView):
       'Print Library Report'
        __name__ = 'library.print_report.start'

   class PrintLibraryReport(Wizard):
       'Print Library Report'
        __name__ = 'library.print_report'

        start = StateView(
            'library.print_report.start', 'library.print_view_form',
            [
                Button('Cancel', 'end', 'tryton-cancel'),
                Button('Print', 'print_', 'tryton-print', default=True),
            ]
        )
        print_ = StateAction('library.book')

        def do_print_(self, action):
            data = {
                'library': self.start.book.id,
            }
            return action, data

        def transition_print_(self):
            return 'end'

Register the  Wizard model name in __init__.py and add the xml
files in tryton.cfg file.

.. code-block:: python

   #Register type_='wizard' in __init__.py
   Pool.register(
      PrintLibraryReport,
      module='library', type_='wizard'
   )

Add the record tag for the wizard in library.xml

.. code-block:: xml

    <record model="ir.action.wizard" id="book_print">
        <field name="name">Print Library Book</field>
        <field name="wiz_name">library.print_report</field>
    </record>


WebServices
-----------

TODO
