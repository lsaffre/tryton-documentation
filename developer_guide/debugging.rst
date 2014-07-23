#################
Debugging Trytond
#################
Tryton is a wonderful platform to work with, populated with equally wonderful
modules. Unfortunately, even the most skilled programmers sometimes make
mistakes, and then comes what developers do 90 % of their time: debugging.

This is what all debugging is about:

  * Find what went wrong
  * Understand why it went wrong

Once the source of the problem is pinpointed, you can correct it. Usually,
correcting a bug without knowing how it appeared will prove useless in the
long run, so one got to be able to discover the core of the problem.

Remember though, a not consistently reproductible bug is your worse nightmare.
This category of bug requires some special treatment that will be detailed in a
dedicated place. The following assumes that your are able to consistently and
easily reproduce the problem.

Tryton Configuration
====================
The tryton server comes bundled with a few options to  make the debugging
easier. Every developement server should have the following setting enabled in
their configuration file:
::

    auto_reload = True

This makes the server reload itself every time one of its resources (python
files, view files...) That allows you to modify your code to ease debugging
with the client running, and restart the action that caused the problem to
either obtain more data on the problem, or to check if a modification you made
changes something.

.. tip::

    Keep in mind though that the modifications that require creating new 
    records in the database to be effective still require a database upgrade.
    That includes adding new fields, creating new records in xml 
    (views / actions...).

Usage of print
==============

The most basic debugging method with python is printing. It is particularly
efficient with the server properly configured as described in the previous
section.

Of course, printing needs to be intelligent to be effective. Usually, you will
want to do the following:

  * Find a context in which the bug arises. This is particularly important when
    the method in which the bug occurs is often used. For instance, when calling
    a method on a list of ids, you need to detect which instance made the method
    crash.
    This can easily be achieved by printing the method arguments at the top of
    the call / the iteration values at the start of a loop. Another option would
    be a try / except around the bad line.
  * Once you can design a test that you are confident allows you to detect the
    problem's context, you can exhaustively use print to get all the context
    information you need to understand what happens.

Server Logging
==============

Use python's logging module to write down useful data for debugging. If you use
the 'DEBUG' loglevel, it will not appear anywhere. It is interesting to use it
in tricky places of the code in which for instance not all cases can be
properly tested.

Currently, the tryton server does not allow easy configuration of the output
log level. To achieve this, you need to edit trytond/server.py and replace
occurences of logging.WARNING with logging.DEBUG in TrytonServer.__init__

Client Logging
==============

The tryton gtk client provides useful fonctionnalities for debugging: debug
mode and verbose mode. Those are arguments on the command line of the tryton
gtk client:
::

    tryton -d -v

The debug mode force the client to fetch the definition of each view you want
to display, every time you want to display it, from the server. That includes
fields definition and xml structure. Useful when your problem is a field
dependency in on_change(_with) / depends. Just change your source, reload the
view (close the current tab and reopen it), and it will be up to date.

The verbose mode is more useful from a debugging point of view.

Every action in the client triggers one / multiple server requests. For
instance, opening a view requires the client to fetch the view definition, the
access right data, the records data, etc. Once you nailed down the action in
the client that triggers the problem, it may trigger tens of requests to the
server, and you got to know which one of those caused the crash. Enabling the
verbose mode will make every request from the client to the server displayed in
the server log this way:
::

    INFO:tryton.rpc:model.model_name.method_name(_, _, arg1, arg2, ..., context)
    DEBUG:tryton.rpc:something

The first arguments of the method call are json-rpc (xml-rpc is similar)
specific parameters like the session token. The answer is the json encoded
method result

Using this properly allows you to know precisely what the server was asked to
do, which is a step toward resolution.

Pdb
===

Pdb_ is the Python Debugger. It may be useful in particularly complex cases, or
when debugging the client itself. It basically provides you a way to place
breakpoints in your code (which is particularly good combined with the server
auto-reloading feature).

Once your running application arrives at the line at which you set the
breakpoint, it stops, and give you the possibility to explore the current
state. It features stack exploration (goin up / down), symbol evaluation, step
by step execution... A good use case is once you know precisely where is the
problem, but you cannot figure out exactly what is going on.

It is no the prefered way to debug as it is some sort of overkill, but
definitely useful in some situations.

Note that for vim users, there exists a python vim binding named Vimpdb_ which
allows to use vim as an interface for pdb, which allows for a better view of
the surrounding code.

.. _Pdb: http://docs.python.org/2/library/pdb.html
.. _Vimpdb: https://github.com/gotcha/vimpdb

Setup trytond for debugging
===========================

There are some traces that are very useful to set up in the server in order to
check for the usual suspects.

Debug those annoying Error 500
------------------------------
In the trytond/protocols/jsonrpc.py file, in SimpleJSONRPCDispatcher._marshaled_dispatch,
you should enclose the 
::

    return json.dumps(response, cls=JSONEncoder)

statement in a try / except + traceback + raise to know what really failed
when you got an error 500 client side.

Know where functional errors where thrown
-----------------------------------------
Add those lines at the start of the raise_user_error method of the
WarningErrorMixin class of the trytond/error.py:
::

    import traceback
    traceback.print_stack()
    
That will make it so that everytime a user error is thrown somewhere in the
server, the server log will print the current stack before displaying the
error to the user.

Debug Functional Errors
-----------------------
Write
::

    print cls.__name__, field_name, value
    
in ModelStorage._validate.required_test (modelstorage.py). This will give
you some info in case of "The field ... is required"

Write
::

    print cls.__name__, field_name, value, test

in ModelStorage._validate at the
cls.raise_user_error('selection_validation_record') line. That way you will
know why "The value ... is not in the selection"

How to deal with non-reproductible errors / client errors
=========================================================
Those are the worst thing you can encounter. The solution for debugging them is
the same: consider you got only one go:

  * When the error occurs server-side and is not reproductible, the only 
    thing you can do is make it so that you get the maximum information out of
    it the few times it occurs.
  * The client does not have the nice autoreload feature of the server (it is
    only possible in the server as it runs separate threads). So everytime you
    change the code, you need to fully restart it. The bottom line is the same:
    you got to make those runs worth it.
    
So basically, use logging extensively. Logging is nice because you can just go on
something else, until the error occurs. Once it does occur, you should be able to
get relevant information about the error context, which hopefully will make it
possible to pinpoint it and understand how to reproduce it.

Another option is to use Pdb_'s post-mortem_ debug mode. This allows you to
try / except your error, then trigger Pdb_ in the except block. Doing so will
make python enter debugging mode in the context of the error when it occurs.

.. _post-mortem : http://docs.python.org/2/library/pdb.html#pdb.post_mortem

Usual errors and how to debug them
=====================================
