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

This approach floods the PyQt code with ugly multi-line strings everywhere.

The *qstylizer* way:

.. code-block:: python

    import qstylizer.style

    css = qstylizer.style.StyleSheet()
    css.QTabBar.border_radius = "3px"
    css.QTabBar.background_color = "green"
    css.QTabBar.focus.border = "0px transparent black"
    css.QTabBar.focus.background_color = "red"
    css.QTabBar.close_button.background = "transparent"

    widget = QtWidgets.QMainWindow()
    widget.setStyleSheet(css.to_string())

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
style property names and the values as the style property values. Any attempt
to get or set a public variable in the instance will add a key and value
into the dictionary (the style rule property:values).

Because a StyleRule is a dictionary, the following is also valid:

.. code-block:: python

    css["QTabBar"]["close-button"]["background"] = "transparent"

If *qstylizer* incorrectly determines that close-button is a pseudostate instead of
a subcontrol, the colons can be specified in the key:

.. code-block:: python

    css.QTabBar["::close-button"].background = "transparent"

What are the advantages? Ease of use and cleaner code. There is no need to
worry about scope operators, brackets, and semi-colons.

