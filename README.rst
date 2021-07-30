*********
qstylizer
*********

.. image:: https://travis-ci.com/blambright/qstylizer.svg?branch=master
    :target: https://www.travis-ci.com/blambright/qstylizer

.. image:: https://readthedocs.org/projects/qstylizer/badge/?version=latest
    :target: http://qstylizer.readthedocs.io/en/latest/?badge=latest

------------
Installation
------------

.. code-block:: bash

    pip install qstylizer

-------------
Documentation
-------------

`Read the Docs <http://qstylizer.readthedocs.io/en/latest/index.html>`_.

------------
Introduction
------------

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
    # The following is also valid and is equivalent to the statement above.
    css["QToolButton::menu-button:pressed"].setValues(**{
        "border": "1px solid #333333",
        "padding": "5px",
        "background-color": "#333333",
    })

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

-------
License
-------

MIT License

Copyright (c) 2018 Brett Lambright

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
