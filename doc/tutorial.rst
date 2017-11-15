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

It is important to note that any name can be used as an attribute.

.. code-block:: python

    >>> css = qstylizer.style.StyleSheet()
    >>> css.QUnknownClass.some_unknown_prop = "none"
    >>> print(css.to_string())
    QUnknownClass {
        some-unknown-prop: none;
    }



Not Operator
------------


Parser
------

