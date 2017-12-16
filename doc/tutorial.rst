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

    >>> css.color.setValue("green")
    >>> css.border.setValue("1px solid red")
    >>> print(css.toString())
    color: green;
    border: 1px solid red;

Global scope vs "* {}"
++++++++++++++++++++++

Adding a sub-style rule will result in a different syntax for the global variables:

.. code-block:: python

    >>> css.color.setValue("green")
    >>> css.border.setValue("1px solid red")
    >>> print(css.toString())
    color: green;
    border: 1px solid red;

    >>> css.QWidget.backgroundColor.setValue("blue")
    >>> print(css.toString())
    * {
        color: green;
        border: 1px solid red;
    }
    QWidget {
        background-color: blue;
    }

Any name can be used as an attribute using brackets.


.. code-block:: python

    >>> css = qstylizer.style.StyleSheet()
    >>> css["QUnknownClass"]["::unknown-subcontrol"]["unknown-prop"].setValue("none")
    >>> print(css.toString())
    QUnknownClass::unknown-subcontrol {
        unknown-prop: none;
    }

Not Operator (!)
++++++++++++++++

.. code-block:: python

    css.QTabBar["!focus"].background.setValue("none")


Parser
++++++

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
    >>> css = qstylizer.parser.parse(stylesheet)
    >>> print(css.QTabBar.focus.toString())
    QTabBar:focus {
        border: 0px transparent black;
        background-color: red;
    }

String Output
+++++++++++++

The *StyleRule.toString()* function call with no parameters will just output
the property:values of that style rule in css format. The
*StyleRule.toString(recursive=True)* function call will output the style rule
and all of the sub-style rules in its hierarchy.

.. code-block:: python

    >>> print(css.QTabBar.toString())
    QTabBar {
        border-radius: 3px;
        background-color: green;
    }
    >>> print(css.QTabBar.toString(recursive=True))
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

