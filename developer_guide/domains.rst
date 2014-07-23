#######
Domains
#######

What is a domain ?
==================

Domains are sets of search criteria. They apply constraints on the model that
is searched so that only a sub-set of its instances are valid regarding the
domain.

You can consider a domain as a filtering expression for your target model. This
is an example of a very basic domain:
::

    [('amount', '>', 0)]

This domain will filter all records whose *amount* field is greater than 0.

A *domain clause* is the building block of a domain. A full domain combines
multiple domain clauses, as well as the *OR* and *AND* operators.
Domain Clause:
::

    ('field_name', 'operator', value, <optional parameter>)

The 'field_name' part of the domain clause is much more than just a field
name. It is possible to chain fields, in order to apply contraints on a
Many2One fields. For instance,
::

    ('invoice.date', '>', Date.today())

is a valid domain.

.. warning:: 
    Though it is theoratically possible to chain fields at will, be carfeul
    that you will still be limited by the database performance. Usually, more
    than two chains (i.e. field1.field2.field3) should be avoided if possible.

Domain (the *AND* operator is implicit between domain clauses):
::

    [domain_clause1, domain_clause2]
    [domain_clause1, ['OR',
        [domain_clause2, domain_clause3],
        [domain_clause4]]]

Domain Usage
============

Domains are everywhere in tryton. As soon as you need to limit the result of a
research on a model, chances is that you are going to need a domain.

Relation Fields
---------------

All relation fields (Many2One, One2Many, Many2Many) support domains. Setting a
domain on a relation field means that the value(s) of the field must comply
with it in order for the record to be valid. For instance:
::

    party = fields.Many2One('party.party', 'Party', domain=[
        ('name', '=', 'John')])

It is now mandatory for all instances of the model in which this field is
defined that its value's name is 'John'.

In administrative tools
-----------------------

Some of Tryton's internal models use domains:
* *Views*
* *Act Windows*
* *Rules*

See the dedicated documentation for details regarding their usage.
.. TODO : Link this to the actual documentation of views / act windows.

Anywhere in the code
--------------------

When using *Model.search(...)*, the first argument you need to pass is a
domain. Almost all the queries that you will write will (and should) use the
search method associated to a domain. Directly building queries through
python-sql, though possible, should be restricted to the case of complex
queries. For instance, aggregate accounting queries would be way to inefficient
if they used the domain pattern as the search function does not provide
aggregate functions.

Advanced Domains
================

Domains support a lot of advanced features which make them very flexible and
adapted to a lot of needs.

Usage of Pyson
--------------

Using Pyson in domains is supported. This is awesome. This allows you to create
dynamic domains depending on, for instance, the value of the current record
field. The context is evaluated as well when computing the domain, so it is
possible to use the active_id in domains set on views.

.. warning:: 
    When using Pyson, be very careful to know what field_names are those of the
    source record (and thus will be evaluated), and which one just represent
    the field names of the target model.

Tuning a domain clause with Pyson:
::

    ('amount', If(Bool(Eval('active')), '>', '<'), 0)

The above domain clause behaves as follow: if the field 'active' of the current
record is *True*, it will accept all target model records for which the field
'amount' is greater than 0. If 'active' evals to *False*, it will accept records
for which the 'amount' is less than 0.
This gives you a wide range of possibilities to define precisely the domain you
need for what you want to do.

Using Pyson to dynamically set the search value:
::

    ('product.category', '=', Eval('category'))

Here, *product.category* is the field on which the domain clause should be
applied. *category* is the current record's category field value.

Tuning a full domain with Pyson:
::

    [(domain_clause1, If(Eval('active'), domain_clause2, domain_clause3))]

You can enclose whole domain clauses in Pyson. A typical use case is to test
whether the record's *id* is set, or if we are working in the scope of a
*company*.

Using the context:
::

    ('company', '=', Eval('context', {}).get('company', None))

Limiting the target record to one which matches the current company is usual,
here is how to do this.

Searcher
--------

Function fields may be used in domains. That is the purpose of the *searcher*
keyword argument in fields.Function. This argument refers to the name of a
function (the searcher function), which transforms a domain_clause using the
function field in a database compatible clause.

For instance, let's assume that the model we are working on has a function
field whose value is the first letter of a *Char* field. The searcher function
will then look like this:
::

    @classmethod
    def search_my_function_field(cls, name, clause):
        return ('my_char_field', clause[1], 
            clause[2][0] if len(clause[2]) else '')

We are basically forwarding the clause from the function field to the actual
char field. We convert the operator part of the clause to only use the first
letter of the search value to match the function field definition.
