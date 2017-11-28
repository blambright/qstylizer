Introduction
============

*qstylizer* is a python package designed to help with the construction of Qt
stylesheets.

The typical way of setting a stylesheet in PyQt is like this:

.. code-block:: python

    widget = QtWidgets.QWidget()
    widget.setStyleSheet("""
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
    """)

This approach floods the python code with ugly multi-line strings everywhere.

The *qstylizer* way:

.. code-block:: python

    import qstylizer.style

    css = qstylizer.style.StyleSheet()
    css.QTabBar.borderRadius = "3px"
    css.QTabBar.backgroundColor = "green"
    css.QTabBar.focus.border = "0px transparent black"
    css.QTabBar.focus.backgroundColor = "red"
    css.QTabBar.closeButton.background = "transparent"

    widget = QtWidgets.QMainWindow()
    widget.setStyleSheet(css.toString())

*qstylizer* stores style rule objects in a dictionary hierarchy.

The above example maps to this hierarchy::

    <StyleSheet dict={
        "QTabBar": <ClassRule name="QTabBar" dict={
            "border-radius": "3px",
            "background-color": "green",
            "focus": <PseudoStateRule name="focus" dict={
                "border": "0px transparent black"
                "background-color": "red"
            } />
            "close-button": <SubControlRule name="close-button" dict={
                "background": "transparent"
            }/>
         } />
    } />

A StyleRule object is basically just an ordered dictionary with the keys as the
style rule property names and the values as the style rule property values. Any
attempt to get or set a public variable in the instance will add a key and value
into the dictionary (the style rule property:values).

Because a StyleRule is a dictionary, the following is also valid:

.. code-block:: python

    css["QTabBar"]["close-button"]["background"] = "transparent"

If *qstylizer* incorrectly determines that close-button is a pseudostate instead
of a subcontrol, the colons can be specified in the key:

.. code-block:: python

    css.QTabBar["::close-button"].background = "transparent"

How Does it Work?
+++++++++++++++++

How does *qstylizer* determine what is a QClass, subcontrol, or pseudostate?
The package itself stores a list of known options for each type.

.. code-block:: python

    >>> qstylizer.style.rule_class("QTabBar")
    <class 'qstylizer.style.ClassRule'>
    >>> qstylizer.style.rule_class("close-button")
    <class 'qstylizer.style.SubControlRule'>
    >>> qstylizer.style.rule_class("hover")
    <class 'qstylizer.style.PseudoStateRule'>


Advantages
++++++++++

What are the advantages? Ease of use and cleaner code. There is no need to
worry about scope operators, brackets, and semi-colons.

*qstylizer* makes it easy to query values of a stylesheet, if necessary.

