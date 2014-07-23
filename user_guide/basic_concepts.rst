Basic Concepts
==============

Tryton is a three-tier high-level general purpose computer application platform
on top of which is built an Enterprise resource planning (ERP) business 
solution through a set of Tryton modules. The three-tiers architecture consists
of the Tryton client, the Tryton server and the Database management system 
(mainly PostgreSQL).

Technical Features
------------------
The client and the server applications are written in Python, the client
use GTK+ as graphical toolkit. Both are available on Linux, OS X.
The kernel provides the technical foundations needed by the most
business applications. However it is not linked to any particular field
hence constituting a general purpose framework:


* Data persistence: ensured by accessor objects called Models, they allow easy 
  creation, migration and access to records.
* User Management: the kernel comes with the base features of user management:
  user groups, access rules by models and records, etc.
* Workflow Engine: allows to activate a workflow on any business model.
* Report Engine: the report engine is based on relatorio that uses ODT files 
  as templates and generate ODT or PDF reports.
* Internationalisation: Tryton is available in English, French, German, 
  Spanish,and Italian. New translations can be added directly from the client 
  interface.
* Historical data: data historization may be enabled on any business model 
  allowing for example to get the list of all the past value of the cost price 
  of any product. It also allows to dynamically access historized record at any 
  time in the past: for instance the customer information on each 
  open invoice will be the ones of the day the invoice was opened.
* Support for DAV protocols: WebDAV, CalDAV, and CardDAV. This allow 
  out-of-the-box document management and synchronizations of calendars and 
  contacts.
* Support for XML-RPC and JSON-RPC protocols.
* Database independence is allowed since the 1.2 series and is used in the 1.4 
  series for the SQLite backend.

Being a framework, Tryton can be used as a platform for the development of 
various other solutions than just business ERPs. A very prominent example is 
GNU Health, a free Health and Hospital Information System based on Tryton.

License
--------
The platform, along with the official modules, are Free Software, licensed 
under the GPLv3.


Product
-------
Basic idea about products


Party
-----

A party can be a person, a company or any organisation that one want to 
consider as the same entity. A party is defined by a name, a code, a language, 
a VAT code, categories, contact mechanisms and a list of addresses.
