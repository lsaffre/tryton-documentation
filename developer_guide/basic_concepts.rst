Basic Concepts
==============



Models
------

:py:class:`~trytond.model.Model([id[,**kwargs]])`
This is the base class that every kind of model inherits.

The most commonly used type of models are:
    - :py:class:`~trytond.model.ModelSQL` (Objects to be stored in an Sql-Database)
    - :py:class:`~trytond.model.ModelView` (Objects to be viewed in the client)
    - :py:class:`~trytond.model.Workflow` (Objects to have different states and state-transitions)

For API-Reference about Models in tryton refer to Trytond docs: :py:mod:`~trytond.model`

Most likely your custom Model will inherit from ModelSql and ModelView at least,
so it can be stored and viewed in the client.

Each :py:class:`~trytond.model.ModelSQL` can hold a set of tryton-fields to represent its attributes.
For a complete list of tryton fields you are refered to Trytond docs: :py:mod:`~trytond.model.fields`


Pool
~~~~

Tryton provides a Pool to serve all your Models in a thread-safe way.
The Pool can contain the following types:

    * model
    * wizard
    * report

You can therefore obtain a model-class from anywhere in your module with the help
of a Pool() instance:

.. code-block:: python

    Books = Pool().get('library.book')  # Model
    book_no_one = Books(1)  # Instance

.. _model-inheritance:

Model Inheritance
~~~~~~~~~~~~~~~~~

To extend an existing model (like Company), one only needs to
instantiate a class with the same __name__ attribute:

.. code-block:: python

    from trytond.model import fields
    from trytond.pool import PoolMeta

    __all__=['Company']
    __metaclass__ = PoolMeta

    class Company:
        __name__ = 'company.company'
        company_code = fields.Char('Company Code')

and register the model to the pool (using a different module name)

.. code-block:: python

    Pool().register(
        Company,
        module='company_something', type='model')

Records
~~~~~~~

Most of trytons behaviour is itself defined by records of internal models (ir).
All records are stored in the database and they can created within the client
or statically predefined in xml files.
When you are unsure about how to define the records, you are encouraged to explore the models
in::

    /trytond
        /ir
        /res



Views
-----

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



Extending Views
~~~~~~~~~~~~~~~

Each inherit view must start with data tag.
**xpath** tag is used which specifies the location where the field is to be
added.

* expr: the xpath expression to find a node in the inherited view.
    * selecting elements starting from "/"
    * selecting one of a set of elements by querying attributes: [@attribute='value']
* position: Define the position of xml-injection.
    * before
    * after
    * replace
    * inside
    * replace_attributes (which will change the attributes)

**Example**

.. code-block:: xml
   :linenos:

        <data>
            <xpath
                expr="/form/notebook/page/separator[@name='signature']"
                position="before">
                <label name="company_code"/>
                <field name="company_code"/>
                <label name="company"/>
                <field name="company"/>
                <label name="employee_code"/>
                <field name="employee_code"/>
            </xpath>
        </data>


Active Records
--------------

TODO





