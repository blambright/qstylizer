*********
qstylizer
*********

.. note:: *qstylizer* is currently a WIP and is not officially released yet.

*qstylizer* is a python package designed to help with the construction of
PyQt/PySide stylesheets.

.. code-block:: python

    import qstylizer.style

    css = qstylizer.style.StyleSheet()
    css.background_color = "green"
    css.color = "#F0F0F0"
    css.margin_left = "2px"
    css.QToolButton.border = "1px transparent lightblue"
    css.QToolButton.border_radius = "3px"
    css.QToolButton.margin = "1px"
    css.QToolButton.padding = "3px"
    css.QToolButton.menu_button.pressed.border = "1px solid #333333"
    css.QToolButton.menu_button.pressed.padding = "5px"
    css.QToolButton.menu_button.background_color = "#333333"

    widget = QtWidgets.QWidget()
    widget.setStyleSheet(css.to_string())

The stylesheet generated above looks like this when passed to setStyleSheet()::

    * {
        background-color: "green";
        color: "#F0F0F0";
        margin-left: "2px";
    }
    QToolButton {
        border: 1px transparent lightblue;
        border-radius: 3px;
        margin: 1px;
        padding: 3px;
    }
    QToolButton::menu-button:pressed {
        border: 1px solid #333333;
        padding: 5px;
        background-color: #333333;
    }

The main advantage of *qstylizer* is cleaner code. No need to flood PyQt/PySide
code with multi-line strings of css. Another advantage is ease of use. There is
no need to care about scope operators, brackets, and colons.

More information to come...

