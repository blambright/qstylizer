Tutorial
========

Creating a StyleSheet
+++++++++++++++++++++

To create a stylesheet, create a :class:`qstylizer.style.StyleSheet` instance.

.. code-block:: python

    >>> import qstylizer.style
    >>> css = qstylizer.style.StyleSheet()

To add global properties, simply start setting values for any attribute.

.. code-block:: python

    >>> css.color.setValue("green")
    >>> css.border.setValue("1px solid red")
    >>> print(css.toString())
    color: green;
    border: 1px solid red;

Here is how to create a style rule for `QTabBar::close-button` and set the
`background` property to `transparent`:

.. code-block:: python

    >>> css.QTabBar.closeButton.background.setValue("transparent")
    >>> print(css.toString())
    * {
        color: green;
        border: 1px solid red;
    }
    QTabBar::close-button {
        background: transparent;
    }

There are actually multiple ways to set a property value. All of the following
statements below are equivalent and valid. Take your pick.

.. code-block:: python

    >>> css.QTabBar.closeButton.background.setValue("transparent")
    >>> css["QTabBar"].closeButton.background.setValue("transparent")
    >>> css["QTabBar"]["close-button"].background.setValue("transparent")
    >>> css["QTabBar"]["close-button"]["background"].setValue("transparent")
    >>> css["QTabBar"]["::close-button"]["background"].setValue("transparent")
    >>> css["QTabBar::close-button"].background.setValue("transparent")
    >>> css["QTabBar::close-button"]["background"].setValue("transparent")


Global scope vs "* {}"
++++++++++++++++++++++

Adding a sub-style rule will result in a different syntax for the global
property values:

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

Unknown Property Names
++++++++++++++++++++++

Any name can be used as an attribute with the use of strings and brackets.

.. code-block:: python

    >>> css = qstylizer.style.StyleSheet()
    >>> css["QUnknownClass::unknown-subcontrol"]["unknown-prop"].setValue("none")
    >>> print(css.toString())
    QUnknownClass::unknown-subcontrol {
        unknown-prop: none;
    }

Not Operator (!)
++++++++++++++++

Here is an example of how to use the `!` operator:

.. code-block:: python

    css.QTabBar["!focus"].background.setValue("none")


Object Property
+++++++++++++++

Here is an example of how to set an object property style rule:

.. code-block:: python

    css['QLineEdit[echoMode="2"]'].background.setValue("none")

Parser
++++++

An existing stylesheet can be converted to a StyleSheet instance as a starting
point. This is handy if you need to change property values in an existing
template stylesheet.

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

The :meth:`qstylizer.style.StyleRule.toString()` function call with no
parameters will just output the property:values of that style rule in css
format. The *qstylizer.style.StyleRule.toString(recursive=True)* function call
will output the style rule and all of the sub-style rules in its hierarchy.

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

