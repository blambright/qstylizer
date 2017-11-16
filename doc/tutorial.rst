Tutorial
========

Creating a StyleSheet
+++++++++++++++++++++

To create a stylesheet, create a :class:`qstylizer.style.StyleSheet` instance.

.. code-block:: python

    >>> import qstylizer.style
    >>> css = qstylizer.style.StyleSheet()

To create a style rule, simply assign an attribute in the instance.

.. code-block:: python

    >>> css.color = "green"
    >>> css.border = "1px solid red"
    >>> print(css.to_string())
    color: green;
    border: 1px solid red;

Global scope vs "* {}"
----------------------

Adding a sub-style rule will result in a different syntax for the global variables:

.. code-block:: python

    >>> css.color = "green"
    >>> css.border = "1px solid red"
    >>> print(css.to_string())
    color: green;
    border: 1px solid red;

    >>> css.QWidget.background_color = "blue"
    >>> print(css.to_string())
    * {
        color: green;
        border: 1px solid red;
    }
    QWidget {
        background-color: blue;
    }

Any name can be used as an attribute.

.. code-block:: python

    >>> css = qstylizer.style.StyleSheet()
    >>> css.QUnknownClass.some_unknown_prop = "none"
    >>> print(css.to_string())
    QUnknownClass {
        some-unknown-prop: none;
    }

Not Operator (!)
----------------

There are two ways to handle the *!* operator.

.. code-block:: python

    css.QTabBar["!focus"].background = "none"

 or

.. code-block:: python

    css.QTabBar.not_focus.background = "none"


Parser
------

An existing stylesheet can be converted to a StyleSheet instance as a starting
point.

.. code-block:: python

    >>> import qstylizer.parser
    >>> stylesheet = """
    ... QTabBar {
    ...     border-radius: 3px;
    ...     background-color: green;
    ... }
    ... QTabBar:focus {
    ...     border: 0px transparent black;
    ...     background-color: red;
    ... }
    ... QTabBar::close-button {
    ...     background: transparent;
    ... }
    ... """
    >>> css = qstylizer.parser.parse_stylesheet(stylesheet)
    >>> print(css.QTabBar.focus.to_string())
    QTabBar:focus {
        border: 0px transparent black;
        background-color: red;
    }

String Output
-------------

The *StyleRule.to_string()* function call with no parameters will just output
the property:values of that style rule in css format. The
*StyleRule.to_string(cascade=True)* function call will output the style rule
and all of the sub-style rules in the hierarchy.

.. code-block:: python

    >>> print(css.QTabBar.to_string())
    QTabBar {
        border-radius: 3px;
        background-color: green;
    }
    >>> print(css.QTabBar.to_string(cascade=True))
    QTabBar {
        border-radius: 3px;
        background-color: green;
    }
    QTabBar:focus {
        border: 0px transparent black;
        background-color: red;
    }
    QTabBar::close-button {
        background: transparent;
    }

