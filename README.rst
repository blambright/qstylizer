*********
qstylizer
*********

.. note:: *qstylizer* is currently a WIP and is not officially released yet.

*qstylizer* is a python package designed to help with the construction of
PyQt/PySide stylesheets.

.. code-block:: python

    import qstylizer.style

    css = qstylizer.style.StyleSheet()
    css.backgroundColor = "green"
    css.color = "#F0F0F0"
    css.marginLeft = "2px"
    css.QToolButton.border = "1px transparent lightblue"
    css.QToolButton.borderRadius = "3px"
    css.QToolButton.margin = "1px"
    css.QToolButton.padding = "3px"
    css.QToolButton.menuButton.pressed.border = "1px solid #333333"
    css.QToolButton.menuButton.pressed.padding = "5px"
    css.QToolButton.menuButton.pressed.backgroundColor = "#333333"

    widget = QtWidgets.QWidget()
    widget.setStyleSheet(css.toString())

The stylesheet generated above looks like this when passed to setStyleSheet()::

    * {
        background-color: green;
        color: #F0F0F0;
        margin-left: 2px;
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

More information to come...

