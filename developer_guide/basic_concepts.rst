Basic Concepts
==============

**Models**


:py:class:`~trytond.model.Model([id[,**kwargs]])`
This is the base class that every kind of model inherits.

The most commonly used type of models are:
    - :py:class:`~trytond.model.ModelSQL` (Objects to be stored in an Sql-Database)
    - :py:class:`~trytond.model.ModelView` (Objects to be viewed in the client)
    - :py:class:`~trytond.model.Workflow` (Objects to have different states and state-transitions)

For API-Reference about Models in tryton refer
to `trytond model docs <http://doc.tryton.org/3.2/trytond/doc/ref/models/models.html>`_

A complete library model is explained in the previous chapter.

Special Functions
-----------------

Most likely your custom Model will inherit from ModelSql and ModelView at least,
so it can be stored and viewed in the client.

Each model can hold a set of tryton-fields to represent its attributes.
For a complete list of tryton fields you are refered to
`trytond docs <http://doc.tryton.org/3.2/trytond/doc/ref/models/fields.html>`_



Default values
^^^^^^^^^^^^^^

You can define default values for fields by adding a 'default_<field_name>' function to your model:

.. code-block:: python

    class Book:
        __name__ = 'library.book'
        renter = fields.Char('Rented by')

        def default_renter():
            return 'me'

Field-Relationships
^^^^^^^^^^^^^^^^^^^

If you have a pair of fields that influence each others value, you may define functions to update
values when a change is detected.

Updating a field should trigger an update on a number of fields
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    * define a function named on_change_<field_name>
    * return a dictionary containing 'field_name': value for all fields to be updated
    * decorate the function with @fields.depends(\*keys) containing all keys to be updated.
      this ensures that all required fields get submitted by the client.


.. code-block:: python

    class Book:
        is_rented_by_me = fields.Boolean('Rented by Me')

        @fields.depends('is_rented_by_me')
        def on_change_renter(self):
            if self.owner == 'me':
                return {'is_rented_by_me': True}
            else:
                return {'is_rented_by_me': False}


Update a field each time a set of fields changes
""""""""""""""""""""""""""""""""""""""""""""""""

    * define a function named on_change_with_<field_B_name>
    * return the fields new value
    * decorate the function with @fields.depends(\*keys) using all the keys that may influence the field

.. code-block:: python

    class Book:
        is_rented_by_me = fields.Boolean('Rented by Me')

        @fields.depends('renter')
        def on_change_with_is_rented_by_me(self):
            return self.renter == 'me'

.. note:: on_change_* and on_change_with_* are called from the client

Function fields
^^^^^^^^^^^^^^^

The previous 'on_change_owner' example could have been solved without storing a new key
to the database and calculating its value on the fly, by adding a function
field:

.. code-block:: python

    class Book:
        is_rented_by_me = fields.Function(fields.Boolean('Rented by Me'), 'get_renter_information')

        def get_renter_information(self, name):
            return self.renter == 'me'

where name is the fields name.
This special field can be accessed just as if it was a normal field
of the type specified but gets computed each time (on the server)

.. note:: function fields are calculated on the server and may be incorrect when a value is changed in the client

Combining on_change with a Function field
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can combine the advantages of Function fields (no extra database-column) and
on_change_* functions (updated in the client) by combining them:

.. code-block:: python

    class Book:
        is_rented_by_me = fields.Function(fields.Boolean('Rented by Me'), 'on_change_with_is_owned_by_me')

        @fields.depends('renter')
        def on_change_with_is_owned_by_me(self, name=None):
             return self.renter == 'me'


Relational Fields
-----------------

Like any `ORM (Object Relational Mapper) <http://en.wikipedia.org/wiki/Object-relational_mapping>`_ Tryton offers relational fields, which enable you
to connect model(s) to its related model(s). You can use any of these:

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

    class Party:
        __name__ = 'party.party'
        rented_books = fields.One2Many('library.book', 'renter', 'Rented Books')

.. note:: The One2Many field requires a Many2One field to be referred in the related Model.


**Views**
=========

The views are used to display records of an object to the user.
In tryton, models can have several views, it is the action, that opens
the window, that tells which views must be used. The view are built using
XML that is stored in the module's view diectory or can be stored in
database with the object.ir.ui.view. So generally, they are defined in xml
files with this kind of xml:

.. code-block:: xml
   :linenos:

    <record model="ir.ui.view" id="view_id">
        <field name="model">model name</field>
        <field name="type">type name</field>
        <field name="inherit" ref="inherit_view_id"/>
    </record>

Active Records
--------------

TODO


Transactions
------------

TODO

Extending Tryton (Inheritance)
------------------------------

Tryton modules can be easily extended. Models and Views need to be
extended using Inheritance.

**Extending Models** : To extend an existing model (like Company), one need to
instantiate a class with the same __name__ attribute:

.. code-block:: python

    from trytond.model import fields
    from trytond.pool import PoolMeta

    __all__=['Company']
    __metaclass__ = PoolMeta


    class Company:
        __name__ = 'company.company'
        company_code = fields.Char('Company Code')


**Extending Views** : Each inherit view must start with data tag.
**xpath** tag is used which specifies the location where the field is to be
added.

* expr : the xpath expression to find a node in the inherited view.
* position : Define the position from the found node, it can be before,
  after, replace, inside or replace_attributes which will change the
  attributes.

**Example**

.. code-block:: xml
   :linenos:

    <data>
        <xpath
            expr="/form/notebook/page/separator[@name=&quot;signature&quot;]"
            position="before">
            <label name="company_code"/>
            <field name="company_code"/>
            <label name="company"/>
            <field name="company"/>
            <label name="employee_code"/>
            <field name="employee_code"/>
        </xpath>
    </data>

Wizard
------------------------------------------------------------------
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
