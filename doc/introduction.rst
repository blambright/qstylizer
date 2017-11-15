Introduction
============

*qstylizer* is a python package designed to help with the construction of Qt
stylesheets.

The typical way of setting a stylesheet in PyQt is like this:

.. code-block:: python

    window = QtWidgets.QMainWindow()
    window.setStyleSheet("""
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
    window = QtWidgets.QMainWindow()
    window.setStyleSheet(css.to_string())

Scope operators, brackets, and semi-colons are handled for you.

