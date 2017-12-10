# coding: utf-8

import pytest
import textwrap


def test_style(css):
    assert css._parent is None
    assert css.QWidget == css.QWidget.item._parent


def test_style_recursive(css):
    css.test = 2
    assert css.test.value == 2
    assert css["test"].value == 2
    css["test"] = 3
    assert css["test"].value == 3
    assert css.test.value == 3
    css.QWidget.color = "green"
    assert css.QWidget.color.value == "green"
    assert css["QWidget"]["color"].value == "green"
    css["QWidget"]["color"] = "blue"
    assert css["QWidget"]["color"].value == "blue"
    assert css.QWidget.color.value == "blue"


def test_delete_style(css):
    css.QWidget.color = "blue"
    assert "color" in css.QWidget.keys()
    del css.QWidget.color
    assert "color" not in css.QWidget.keys()
    css.QWidget["color"] = "blue"
    assert "color" in css.QWidget.keys()
    del css.QWidget["color"]
    assert "color" not in css.QWidget.keys()


def test_subcontrol(css):
    import qstylizer.style
    assert type(css.QWidget.item) == qstylizer.style.SubControlRule


def test_pseudo_state(css):
    import qstylizer.style
    assert type(css.QWidget.item.selected) == qstylizer.style.PseudoStateRule


def test_selector(css):
    assert css.QCheckBox.indicator.selector == "QCheckBox::indicator"
    assert css.QCheckBox.indicator.unchecked.selector == "QCheckBox::indicator:unchecked"
    assert css.QCheckBox.indicator.unchecked.hover.selector == "QCheckBox::indicator:unchecked:hover"
    assert css.Object.subcontrol.pseudostate.selector == "Object::subcontrol:pseudostate"
    assert css["Object::subcontrol:pseudostate"].selector == "Object::subcontrol:pseudostate"
    assert css.QLineEdit['[echoMode="2"]'].selector == "QLineEdit[echoMode=\"2\"]"
    assert css.Object["::subcontrol"][":pseudostate"].selector == "Object::subcontrol:pseudostate"
    assert css["QWidget#objectName"].selector == "QWidget#objectName"


def test_style_list(css):
    css["QCheckBox, QLineEdit, QFrame"].border = "none"
    css["QWidget,#objectName"].border = "none"
    css["*,\nQCheckBox::subcontrol:pseudostate"].margin = "none"
    assert "QCheckBox" in css.keys()
    assert "QLineEdit" in css.keys()
    assert "QWidget" in css.keys()
    assert "#objectName" in css.keys()
    assert "border" in css.QWidget.keys()
    assert "border" in css.QLineEdit.keys()
    assert "margin" in css["QCheckBox::subcontrol:pseudostate"].keys()
    assert css.toString() == textwrap.dedent(
        """
        QCheckBox {
            border: none;
        }
        QLineEdit {
            border: none;
        }
        QFrame {
            border: none;
        }
        QWidget {
            border: none;
        }
        #objectName {
            border: none;
        }
        * {
            margin: none;
        }
        QCheckBox::subcontrol:pseudostate {
            margin: none;
        }
        """
    )[1:]


def test_style_style(css):
    css.QCheckBox.indicator.unchecked.hover.border = "none"
    css.QCheckBox.indicator.unchecked.hover.color = "green"
    assert css.QCheckBox.indicator.unchecked.hover.toString() == \
           "QCheckBox::indicator:unchecked:hover {\n    border: none;\n    color: green;\n}\n"


def test_to_string_recursive(css):
    css.border = "none"
    css.QFrame.border = "1px solid green"
    css.QFrame.color = "green"
    css.QCheckBox.border = "1px solid green"
    css.QCheckBox.color = "green"
    css.QCheckBox.indicator.backgroundColor = "red"
    css.QCheckBox.indicator.unchecked.border = "none"
    css.QCheckBox.indicator.unchecked.backgroundColor = "rgb(0,20,0)"
    css.QCheckBox.indicator.unchecked.hover.backgroundColor = "purple"
    css.QLineEdit['[echoMode="2"]'].lineeditPasswordCharacter = 9679
    css["QCheckBox::indicator:unchecked"].margin = 0
    assert css.toString() == textwrap.dedent(
        """
        * {
            border: none;
        }
        QFrame {
            border: 1px solid green;
            color: green;
        }
        QCheckBox {
            border: 1px solid green;
            color: green;
        }
        QCheckBox::indicator {
            background-color: red;
        }
        QCheckBox::indicator:unchecked {
            border: none;
            background-color: rgb(0,20,0);
            margin: 0;
        }
        QCheckBox::indicator:unchecked:hover {
            background-color: purple;
        }
        QLineEdit[echoMode="2"] {
            lineedit-password-character: 9679;
        }
        """
    )[1:]


def test_empty_style(css):
    css.QCheckBox.indicator.border = "none"
    assert css.QCheckBox.toString() == ""


def test_subcontrol_options():
    import qstylizer.descriptor.subcontrol
    assert 'add-line' in qstylizer.descriptor.subcontrol.SubControlParent.get_attr_options()


def test_pseudostate_options():
    import qstylizer.descriptor.pseudostate
    assert 'minimized' in qstylizer.descriptor.pseudostate.PseudoStateParent.get_attr_options()


def test_prop_semicolon(css):
    css.QComboBox.color = "red;"
    assert css.QComboBox.color.value == "red"


# def test_deepcopy(css):
#     import copy
#     css.QCheckBox.indicator.hover.border = "none"
#     css.QCheckBox.indicator.backgroundColor = "red"
#     indicator = copy.deepcopy(css.QCheckBox.indicator)
#     indicator.color = "yellow"
#     indicator.hover.border = "1px solid green"
#     assert indicator is not css.QCheckBox.indicator
#     assert "color" in indicator.keys()
#     assert "color" not in css.QCheckBox.indicator.keys()
#     assert css.QCheckBox.indicator.hover.border == "none"
#     assert indicator.hover.border == "1px solid green"
#
#
# def test_assign_subcontrol(css):
#     import qstylizer.style
#     subcontrol = qstylizer.style.SubControlRule("indicator")
#     subcontrol.backgroundColor = "red"
#     subcontrol.unchecked.border = "none"
#     subcontrol.unchecked.backgroundColor = "rgb(0,20,0)"
#     subcontrol.unchecked.hover.backgroundColor = "purple"
#
#     css.QComboBox.indicator = subcontrol
#     css.QCheckBox.indicator = subcontrol
#
#     assert css.QCheckBox.indicator is not css.QComboBox.indicator
#     assert css.QCheckBox.indicator.selector == "QCheckBox::indicator"
#     assert css.QComboBox.indicator.selector == "QComboBox::indicator"


def test_child_class_style(css):
    css.QWidget.color = "red"
    css["QWidget QFrame"].backgroundColor = "green"
    css.QFrame.color = "black"
    assert css.toString() == textwrap.dedent(
        """
        QWidget {
            color: red;
        }
        QWidget QFrame {
            background-color: green;
        }
        QFrame {
            color: black;
        }
        """
    )[1:]


def test_unscoped_style(css):
    css.backgroundColor = "red"
    css.border = "none"
    assert css.toString() == textwrap.dedent(
        """
        background-color: red;
        border: none;
        """
    )[1:]


def test_global_style(css):
    css.backgroundCcolor = "red"
    css.border = "none"
    css.QWidget.indicator.border = "1px solid green"
    print css.toString() == textwrap.dedent(
        """
        * {
            background-color: red;
            border: none;
        }
        QWidget::indicator {
            border: 1px solid green;
        }
        """
    )[1:]


def test_not_operator(css):
    import qstylizer.style
    css.QWidget.indicator["!selected"].color = "green"
    assert type(css.QWidget.indicator["!selected"]) == qstylizer.style.PseudoStateRule
    assert css.toString() == textwrap.dedent(
        """
        QWidget::indicator:!selected {
            color: green;
        }
        """
    )[1:]


def test_getattr_not(css):
    import qstylizer.style
    css.QWidget.indicator.notSelected.color = "green"
    assert type(css.QWidget.indicator.notSelected) == qstylizer.style.PseudoStateRule
    assert css.toString() == textwrap.dedent(
        """
        QWidget::indicator:!selected {
            color: green;
        }
        """
    )[1:]


def test_pseudostate_prop_same_name(css):
    css.QWidget.top = 0
    css.QWidget.right = 0
    css.QWidget.bottom = 0
    css.QWidget.left = 0
    css.QTabBar.tab.top.color = "red"
    assert css.toString() == textwrap.dedent(
        """
        QWidget {
            top: 0;
            right: 0;
            bottom: 0;
            left: 0;
        }
        QTabBar::tab:top {
            color: red;
        }
        """
    )[1:]


def test_pseudoprop_set(css):
    css.QWidget.tab.top = "0"
    css.QWidget.tab.top.color = "green"
    assert css.toString() == textwrap.dedent(
        """
        QWidget::tab {
            top: 0;
        }
        QWidget::tab:top {
            color: green;
        }
        """
    )[1:]


def test_add_rule(css):
    css.QCheckBox.indicator.backgroundColor = "red"
    assert len(css._rules) == 3
    assert css.QCheckBox in css._rules.values()
    assert css.QCheckBox.indicator in css._rules.values()
