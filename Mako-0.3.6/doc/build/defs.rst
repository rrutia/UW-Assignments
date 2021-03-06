.. _defs_toplevel:

====
Defs
====

``<%def>`` is the single tag used to demarcate any block of text
and/or code. It exists within generated Python as a callable
function:

.. sourcecode:: mako

    <%def name="hello()">
        hello world
    </%def>

They are normally called as expressions:

.. sourcecode:: mako

    the def:  ${hello()}

If the ``<%def>`` is not nested inside of another ``<%def>``,
its known as a **top level def** and can be accessed anywhere in
the template, including above where it was defined.

All defs, top level or not, have access to the current
contextual namespace in exactly the same way their containing
template does. Suppose the template below is executed with the
variables ``username`` and ``accountdata`` inside the context:

.. sourcecode:: mako

    Hello there ${username}, how are ya.  Lets see what your account says:
    
    ${account()}

    <%def name="account()">
        Account for ${username}:<br/>
    
        % for row in accountdata:
            Value: ${row}<br/>
        % endfor
    </%def>

The ``username`` and ``accountdata`` variables are present
within the main template body as well as the body of the
``account()`` def.

Since defs are just Python functions, you can define and pass
arguments to them as well:

.. sourcecode:: mako

    ${account(accountname='john')}
    
    <%def name="account(accountname, type='regular')">
        account name: ${accountname}, type ${type}
    </%def>

When you declare an argument signature for your def, they are
required to follow normal Python conventions (i.e., all
arguments are required except keyword arguments with a default
value). This is in contrast to using context-level variables,
which evaluate to ``UNDEFINED`` if you reference a name that
does not exist.

Calling defs from Other Files 
==============================

Top level ``<%defs>`` are **exported** by your template's
module, and can be called from the outside; including from other
templates, as well as normal Python code. Calling a ``<%def>``
from another template is something like using an ``<%include>``
- except you are calling a specific function within the
template, not the whole template.

The remote ``<%def>`` call is also a little bit like calling
functions from other modules in Python. There is an "import"
step to pull the names from another template into your own
template; then the function or functions are available.

To import another template, use the ``<%namespace>`` tag:

.. sourcecode:: mako

    <%namespace name="mystuff" file="mystuff.html"/>

The above tag adds a local variable "mystuff" to the current
scope.

Then, just call the defs off of ``mystuff``:

.. sourcecode:: mako

    ${mystuff.somedef(x=5,y=7)}

The ``<%namespace>`` tag also supports some of the other
semantics of Python's ``import`` statement, including pulling
names into the local variable space, or using ``*`` to represent
all names, using the ``import`` attribute:

.. sourcecode:: mako

    <%namespace file="mystuff.html" import="foo, bar"/>

This is just a quick intro to the concept of a **namespace**,
which is a central Mako concept that has its own chapter in
these docs. For more detail and examples, see
:ref:`namespaces_toplevel`.

Calling defs programmatically
==============================

You can call def's programmatically from any :class:`.Template` object
using the :meth:`~.Template.get_def()` method, which returns a :class:`.DefTemplate`
object. This is a :class:`.Template` subclass which the parent
:class:`.Template` creates, and is usable like any other template:

.. sourcecode:: python

    from mako.template import Template
    
    template = Template("""
        <%def name="hi(name)">
            hi ${name}!
        </%def>
        
        <%def name="bye(name)">
            bye ${name}!
        </%def>
    """)
    
    print template.get_def("hi").render(name="ed")
    print template.get_def("bye").render(name="ed")
    

Defs within Defs
================

The def model follows regular Python rules for closures.
Declaring ``<%def>`` inside another ``<%def>`` declares it
within the parent's **enclosing scope**:

.. sourcecode:: mako

    <%def name="mydef()">
        <%def name="subdef()">
            a sub def
        </%def>
        
        im the def, and the subcomponent is ${subdef()}
    </%def>

Just like Python, names that exist outside the inner ``<%def>``
exist inside it as well:

.. sourcecode:: mako

    <%
        x = 12
    %>
    <%def name="outer()">
        <%
            y = 15
        %>
        <%def name="inner()">
            inner, x is ${x}, y is ${y}
        </%def>

        outer, x is ${x}, y is ${y}
    </%def>

Assigning to a name inside of a def declares that name as local
to the scope of that def (again, like Python itself). This means
the following code will raise an error:

.. sourcecode:: mako

    <%
        x = 10
    %>
    <%def name="somedef()">
        ## error !
        somedef, x is ${x}  
        <%
            x = 27  
        %>
    </%def>

...because the assignment to ``x`` declares x as local to the
scope of ``somedef``, rendering the "outer" version unreachable
in the expression that tries to render it.

.. _defs_with_content:

Calling a def with embedded content and/or other defs
=====================================================

A flip-side to def within def is a def call with content. This
is where you call a def, and at the same time declare a block of
content (or multiple blocks) that can be used by the def being
called. The main point of such a call is to create custom,
nestable tags, just like any other template language's
custom-tag creation system - where the external tag controls the
execution of the nested tags and can communicate state to them.
Only with Mako, you don't have to use any external Python
modules, you can define arbitrarily nestable tags right in your
templates.

To achieve this, the target def is invoked using the form
``<%namepacename:defname>`` instead of the normal ``${}``
syntax. This syntax, introduced in Mako 0.2.3, is functionally
equivalent another tag known as ``call``, which takes the form
``<%call expr='namespacename.defname(args)'>``. While ``%call``
is available in all versions of Mako, the newer style is
probably more familiar looking. The ``namespace`` portion of the
call is the name of the **namespace** in which the def is
defined - in the most simple cases, this can be ``local`` or
``self`` to reference the current template's namespace (the
difference between ``local`` and ``self`` is one of inheritance
- see :ref:`namespaces_builtin` for details).

When the target def is invoked, a variable ``caller`` is placed
in its context which contains another namespace containing the
body and other defs defined by the caller. The body itself is
referenced by the method ``body()``. Below, we build a ``%def``
that operates upon ``caller.body()`` to invoke the body of the
custom tag:

.. sourcecode:: mako

    <%def name="buildtable()">
        <table>
            <tr><td>
                ${caller.body()}
            </td></tr>
        </table>
    </%def>
    
    <%self:buildtable>
        I am the table body.
    </%self:buildtable>
    
This produces the output (whitespace formatted):

.. sourcecode:: html

    <table>
        <tr><td>
            I am the table body.
        </td></tr>
    </table>

Using the older ``%call`` syntax looks like:

.. sourcecode:: mako

    <%def name="buildtable()">
        <table>
            <tr><td>
                ${caller.body()}
            </td></tr>
        </table>
    </%def>

    <%call expr="buildtable()">
        I am the table body.
    </%call>

The ``body()`` can be executed multiple times or not at all.
This means you can use def-call-with-content to build iterators,
conditionals, etc:

.. sourcecode:: mako

    <%def name="lister(count)">
        % for x in range(count):
            ${caller.body()}
        % endfor
    </%def>
    
    <%self:lister count="${3}">
        hi
    </%self:lister>
    
Produces:
    
.. sourcecode:: html

    hi
    hi
    hi

Notice above we pass ``3`` as a Python expression, so that it
remains as an integer.

A custom "conditional" tag:
    
.. sourcecode:: mako

    <%def name="conditional(expression)">
        % if expression:
            ${caller.body()}
        % endif
    </%def>

    <%self:conditional expression="${4==4}">
        im the result
    </%self:conditional>

Produces:

.. sourcecode:: html

    im the result

But that's not all. The ``body()`` function also can handle
arguments, which will augment the local namespace of the body
callable. The caller must define the arguments which it expects
to receive from its target def using the ``args`` attribute,
which is a comma-separated list of argument names. Below, our
``<%def>`` calls the ``body()`` of its caller, passing in an
element of data from its argument:

.. sourcecode:: mako

    <%def name="layoutdata(somedata)">
        <table>
        % for item in somedata:
            <tr>
            % for col in item:
                <td>${caller.body(col=col)}</td>
            % endfor
            </tr>
        % endfor
        </table>
    </%def>

    <%self:layoutdata somedata="${[[1,2,3],[4,5,6],[7,8,9]]}" args="col">\
    Body data: ${col}\
    </%self:layoutdata>
    
Produces:

.. sourcecode:: html

    <table>
       <tr>
           <td>Body data: 1</td>
           <td>Body data: 2</td>
           <td>Body data: 3</td>
       </tr>
       <tr>
           <td>Body data: 4</td>
           <td>Body data: 5</td>
           <td>Body data: 6</td>
       </tr>
       <tr>
           <td>Body data: 7</td>
           <td>Body data: 8</td>
           <td>Body data: 9</td>
       </tr>
    </table>
    
You don't have to stick to calling just the ``body()`` function.
The caller can define any number of callables, allowing the
``<%call>`` tag to produce whole layouts:

.. sourcecode:: mako

    <%def name="layout()">
        ## a layout def
        <div class="mainlayout">
            <div class="header">
                ${caller.header()}
            </div>
            <div class="sidebar">
                ${caller.sidebar()}
            </div>
            <div class="content">
                ${caller.body()}
            </div>
        </div>
    </%def>

    ## calls the layout def
    <%self:layout>
        <%def name="header()">
            I am the header
        </%def>
        <%def name="sidebar()">
            <ul>
                <li>sidebar 1</li>
                <li>sidebar 2</li>
            </ul>
        </%def>
        
            this is the body
    </%self:layout>
    
The above layout would produce:

.. sourcecode:: html

    <div class="mainlayout">
       <div class="header">
       I am the header
       </div>

       <div class="sidebar">
       <ul>
           <li>sidebar 1</li>
           <li>sidebar 2</li>
       </ul>
       </div>

       <div class="content">
       this is the body
       </div>
    </div>

The number of things you can do with ``<%call>`` and/or the
``<%namespacename:defname>`` calling syntax is enormous. You can
create form widget libraries, such as an enclosing ``<FORM>``
tag and nested HTML input elements, or portable wrapping schemes
using ``<div>`` or other elements. You can create tags that
interpret rows of data, such as from a database, providing the
individual columns of each row to a ``body()`` callable which
lays out the row any way it wants. Basically anything you'd do
with a "custom tag" or tag library in some other system, Mako
provides via ``<%def>`` tags and plain Python callables which are
invoked via ``<%namespacename:defname>`` or ``<%call>``.



