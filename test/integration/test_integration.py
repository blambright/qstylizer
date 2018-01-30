# coding: utf-8

import pytest
import textwrap


def test_style(css):
    assert css._parent is None
    assert css.QWidget == css.QWidget.item._parent


def test_style_recursive(css):
    css["test"].setValue(3)
    assert css["test"].value == 3
    css.QWidget.color.setValue("green")
    assert css.QWidget.color.value == "green"
    assert css["QWidget"]["color"].value == "green"
    css["QWidget"]["color"].setValue("blue")
    assert css["QWidget"]["color"].value == "blue"
    assert css.QWidget.color.value == "blue"


def test_delete_style(css):
    css.QWidget.color.setValue("blue")
    assert "color" in css.QWidget.keys()
    del css.QWidget.color
    assert "color" not in css.QWidget.keys()
    css.QWidget["color"].setValue("blue")
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
    assert css["Object"]["subcontrol"]["pseudostate"].selector == "Object::subcontrol:pseudostate"
    assert css["Object::subcontrol:pseudostate"].selector == "Object::subcontrol:pseudostate"
    assert css.QLineEdit['[echoMode="2"]'].selector == "QLineEdit[echoMode=\"2\"]"
    assert css["Object"]["::subcontrol"][":pseudostate"].selector == "Object::subcontrol:pseudostate"
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
        * {
            margin: none;
        }
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
        QCheckBox::subcontrol:pseudostate {
            margin: none;
        }
        """
    )[1:]


def test_style_style(css):
    css.QCheckBox.indicator.unchecked.hover.border.setValue("none")
    css.QCheckBox.indicator.unchecked.hover.color.setValue("green")
    assert css.QCheckBox.indicator.unchecked.hover.toString() == \
           "QCheckBox::indicator:unchecked:hover {\n    border: none;\n    color: green;\n}\n"


def test_to_string_recursive(css):
    css.border.setValue("none")
    css.QFrame.border.setValue("1px solid green")
    css.QFrame.color.setValue("green")
    css.QCheckBox.border.setValue("1px solid green")
    css.QCheckBox.color.setValue("green")
    css.QCheckBox.indicator.backgroundColor.setValue("red")
    css.QCheckBox.indicator.unchecked.border.setValue("none")
    css.QCheckBox.indicator.unchecked.backgroundColor.setValue("rgb(0,20,0)")
    css.QCheckBox.indicator.unchecked.hover.backgroundColor.setValue("purple")
    css.QLineEdit['[echoMode="2"]']["lineedit-password-character"].setValue(9679)
    css["QCheckBox::indicator:unchecked"].margin.setValue(0)
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
    css.QCheckBox.indicator.border.setValue("none")
    assert css.QCheckBox.toString() == ""


def test_subcontrol_options():
    import qstylizer.descriptor.subcontrol
    assert 'add-line' in qstylizer.descriptor.subcontrol.SubControlParent.get_attr_options()


def test_pseudostate_options():
    import qstylizer.descriptor.pseudostate
    assert 'minimized' in qstylizer.descriptor.pseudostate.PseudoStateParent.get_attr_options()


def test_prop_semicolon(css):
    css.QComboBox.color.setValue("red;")
    assert css.QComboBox.color.value == "red"


# def test_deepcopy(css):
#     import copy
#     css.QCheckBox.indicator.hover.border.setValue("none"
#     css.QCheckBox.indicator.backgroundColor.setValue("red"
#     indicator.setValue(copy.deepcopy(css.QCheckBox.indicator)
#     indicator.color.setValue("yellow"
#     indicator.hover.border.setValue("1px solid green"
#     assert indicator is not css.QCheckBox.indicator
#     assert "color" in indicator.keys()
#     assert "color" not in css.QCheckBox.indicator.keys()
#     assert css.QCheckBox.indicator.hover.border == "none"
#     assert indicator.hover.border == "1px solid green"
#
#
# def test_assign_subcontrol(css):
#     import qstylizer.style
#     subcontrol.setValue(qstylizer.style.SubControlRule("indicator")
#     subcontrol.backgroundColor.setValue("red"
#     subcontrol.unchecked.border.setValue("none"
#     subcontrol.unchecked.backgroundColor.setValue("rgb(0,20,0)"
#     subcontrol.unchecked.hover.backgroundColor.setValue("purple"
#
#     css.QComboBox.indicator.setValue(subcontrol
#     css.QCheckBox.indicator.setValue(subcontrol
#
#     assert css.QCheckBox.indicator is not css.QComboBox.indicator
#     assert css.QCheckBox.indicator.selector == "QCheckBox::indicator"
#     assert css.QComboBox.indicator.selector == "QComboBox::indicator"


def test_child_class_style(css):
    css.QWidget.color.setValue("red")
    css["QWidget QFrame"].backgroundColor.setValue("green")
    css.QFrame.color.setValue("black")
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
    css.backgroundColor.setValue("red")
    css.border.setValue("none")
    assert css.toString() == textwrap.dedent(
        """
        background-color: red;
        border: none;
        """
    )[1:]


def test_global_style(css):
    css.backgroundColor.setValue("red")
    css.border.setValue("none")
    css.QWidget.indicator.border.setValue("1px solid green")
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
    css.QWidget.indicator["!selected"].color.setValue("green")
    assert type(css.QWidget.indicator["!selected"]) == qstylizer.style.PseudoStateRule
    assert css.toString() == textwrap.dedent(
        """
        QWidget::indicator:!selected {
            color: green;
        }
        """
    )[1:]


def test_pseudostate_prop_same_name(css):
    css.QWidget.top.setValue(0)
    css.QWidget.right.setValue(0)
    css.QWidget.bottom.setValue(0)
    css.QWidget.left.setValue(0)
    css.QTabBar.tab.top.color.setValue("red")
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
    css.QWidget.tab.top.setValue("0")
    css.QWidget.tab.top.color.setValue("green")
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


def test_add_child_rule(css):
    css.QCheckBox.indicator.backgroundColor.setValue("red")
    assert len(css._child_rules) == 3
    assert css.QCheckBox in css._child_rules.values()
    assert css.QCheckBox.indicator in css._child_rules.values()


def test_set_values(css):
    css.QToolButton.setValues(
        border="1px transparent lightblue",
        borderRadius="3px",
        margin="1px",
        padding="3px",
    )
    assert css.QToolButton.border.value == "1px transparent lightblue"


def test_global_object_prop(css):
    css["*"].color.setValue("green")
    css["*[test=\"2\"]"].color.setValue("red")
    assert css.toString() == textwrap.dedent(
        """
        * {
            color: green;
        }
        *[test="2"] {
            color: red;
        }
        """
    )[1:]


def test_global_scope(css):
    css["*"].color.setValue("red")
    css.backgroundColor.setValue("green")
    assert css.toString() == textwrap.dedent(
        """
        * {
            color: red;
            background-color: green;
        }
        """
    )[1:]
