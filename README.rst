*********
qstylizer
*********

.. note:: *qstylizer* is currently a WIP and is not officially released yet.

*qstylizer* is a python package designed to help with the construction of
PyQt/PySide stylesheets.

.. code-block:: python

    import qstylizer.style

    css = qstylizer.style.StyleSheet()
    css.setValues(
        backgroundColor="green",
        color="#F0F0F0",
        marginLeft="2px"
    )
    css.QToolButton.setValues(
        border="1px transparent lightblue",
        borderRadius="3px",
        margin="1px",
        padding="3px"
    )
    css.QToolButton.menuButton.pressed.setValues(
        border="1px solid #333333",
        padding="5px",
        backgroundColor="#333333"
    )
    QCheckBox.disabled.backgroundColor.setValue("#797979")

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
    QCheckBox:disabled {
        background-color: #797979;
    }

More information to come...

