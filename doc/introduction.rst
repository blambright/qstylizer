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
    css.QTabBar.setValues(
        borderRadius="3px",
        backgroundColor="green"
    )
    css.QTabBar.focus.setValues(
        border="0px transparent black",
        backgroundColor="red"
    )
    css.QTabBar.closeButton.background.setValue("transparent")

    widget = QtWidgets.QMainWindow()
    widget.setStyleSheet(css.toString())

*qstylizer* stores style rule objects in a dictionary hierarchy.

The above example maps to this hierarchy::

    <StyleSheet dict={
        "QTabBar": <ClassRule name="QTabBar" dict={
            "border-radius": <PropRule name="border-radius" value="3px" />,
            "background-color": <PropRule name="background-color" value="green" />,
            "focus": <PseudoStateRule name="focus" dict={
                "border": <PropRule name="border" value="0px transparent black" />,
                "background-color": <PropRule name="background-color" value="red" />,
            } />
            "close-button": <SubControlRule name="close-button" dict={
                "background": <PropRule name="background" value="transparent" />,
            }/>
         } />
    } />

A StyleRule object is basically just an ordered dictionary with the keys as the
style rule property names and the values as the style rule property values. Any
attempt to get a dictionary value in the instance will add a key and value
into the dictionary (the style rule property:values).

If *qstylizer* incorrectly determines that close-button is a pseudostate instead
of a subcontrol, the colons can be specified in the key:

.. code-block:: python

    css.QTabBar["::close-button"].background.setValue("transparent")

Because of the hierarchical nature, the following are all valid:

.. code-block:: python

    css.QTabBar.closeButton.background.setValue("transparent")
    css["QTabBar"].closeButton.background.setValue("transparent")
    css["QTabBar"]["close-button"].background.setValue("transparent")
    css["QTabBar"]["close-button"]["background"].setValue("transparent")
    css["QTabBar"]["::close-button"]["background"].setValue("transparent")
    css["QTabBar::close-button"].background.setValue("transparent")
    css["QTabBar::close-button"]["background"].setValue("transparent")

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
