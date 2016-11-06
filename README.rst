=========
Documents
=========


**Documents** is a simple template engine built on top of Jinja2_ and built with Click_. It turns your
templates into interactive cli applications and returns a rendered document ready to be saved.

Installation
============

#. Clone the repository
#. Run `python setup.py install`

Usage
=====

Quick use
---------

To use **Documents** simply run `documents` from you command line. For additional information 
run `documents --help`.

Detailed
--------

What the app does is it looks into your templates directory - the default directory is `./templates` - 
and returns the list of your templates.

Templates can be HTML, md, rst or any text files you wish, regardless of their markup. What makes them templates 
is the use of the Jinja2 markup language. The basic idea is that variables are encapsulated with curly brackets 
`{{ }}`. 

There is of course a lot more to it, and tons of options, like template inheritance, so I encourage you to 
read Jinja2's documentation_.

When the app get's a template it looks for its variables and turns them into "prompts" (`click.prompt()` 
methods_ to be exact). Once the user enters all the variables, the app crates a dict and renders the template 
with it.

TODO: saving
============

For now the app has no save option. But one will be added soon. Till then I recomend using a pipe.

MISC
====

I'll be doing a Flask app and a Flask Rest API with a simple JS frontend in the future, so you won't be stuck 
with the cli version.

If you have any suggestions or just feel like talking, find me on Twtitter: @dasdachs_.

Cheers!

.. _Jinja2: http://jinja.pocoo.org/
.. _Click: http://click.pocoo.org/
.. _documentation: http://jinja.pocoo.org/
.. _methods: http://click.pocoo.org/5/prompts/
.. _@dasdachs: https://twitter.com/dasdachs
