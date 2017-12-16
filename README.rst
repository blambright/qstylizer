*********
qstylizer
*********

*qstylizer* is a python package designed to help with the construction of
PyQt/PySide stylesheets.

.. code-block:: python

    import PyQt5.QtWidgets

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
    css.QCheckBox.disabled.backgroundColor.setValue("#797979")

    widget = PyQt5.QtWidgets.QWidget()
    widget.setStyleSheet(css.toString())

The stylesheet generated above looks like this when passed to setStyleSheet()::

    * {
        color: #F0F0F0;
        margin-left: 2px;
        background-color: green;
    }
    QToolButton {
        border-radius: 3px;
        padding: 3px;
        border: 1px transparent lightblue;
        margin: 1px;
    }
    QToolButton::menu-button:pressed {
        padding: 5px;
        border: 1px solid #333333;
        background-color: #333333;
    }
    QCheckBox:disabled {
        background-color: #797979;
    }

The true power comes from parsing an existing stylesheet and tweaking individual
property values.

.. code-block:: python

    import qstylizer.parser

    css = qstylizer.parser.parse(
        """
        QToolButton::menu-button:pressed {
            padding: 5px;
            border: 1px solid #333333;
            background-color: #333333;
        }
        QCheckBox:disabled {
            background-color: #797979;
        }
        """
    )
    css.QToolButton.menuButton.pressed.padding.setValue("10px")
    css.QCheckBox.disabled.backgroundColor.setValue("#222222")

    print(css.toString())

Output::

    QToolButton::menu-button:pressed {
        padding: 10px;
        border: 1px solid #333333;
        background-color: #333333;
    }
    QCheckBox:disabled {
        background-color: #222222;
    }

