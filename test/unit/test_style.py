
import pytest


@pytest.fixture
def css():
    import qstylizer.style
    # css = qstylizer.style.Style()
    return qstylizer.style.Style()


def test_style(css):
    assert css._parent is None
    assert css.QWidget == css.QWidget.item._parent


def test_style_cascade(css):
    css.value = 2
    assert css.value == 2
    assert css["value"] == 2
    css["value"] = 3
    assert css["value"] == 3
    assert css.value == 3
    css.QWidget.color = "green"
    assert css.QWidget.color == "green"
    assert css["QWidget"]["color"] == "green"
    css["QWidget"]["color"] = "blue"
    assert css["QWidget"]["color"] == "blue"
    assert css.QWidget.color == "blue"


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
    assert type(css.QWidget.item) == qstylizer.style.SubControl


def test_pseudo_state(css):
    import qstylizer.style
    assert type(css.QWidget.item.selected) == qstylizer.style.PseudoState


def test_identifier(css):
    assert css.QCheckBox.indicator.identifier == "QCheckBox::indicator"
    assert css.QCheckBox.indicator.unchecked.identifier == "QCheckBox::indicator:unchecked"
    assert css.QCheckBox.indicator.unchecked.hover.identifier == "QCheckBox::indicator:unchecked:hover"
    assert css.Object.subcontrol.pseudostate.identifier == "Object::subcontrol:pseudostate"
    assert css["Object::subcontrol:pseudostate"].identifier == "Object::subcontrol:pseudostate"
    assert css.QLineEdit['[echoMode="2"]'].identifier == "QLineEdit[echoMode=\"2\"]"
    assert css.Object["::subcontrol"][":pseudostate"].identifier == "Object::subcontrol:pseudostate"
    assert css["QWidget#objectName"].identifier == "QWidget#objectName"


def test_style_list(css):
    css["QCheckBox, QLineEdit, QFrame"].border = "none"
    css["QWidget,#objectName"].border = "none"
    css["*,QCheckBox::subcontrol:pseudostate"].margin = "none"
    assert "QCheckBox" in css.keys()
    assert "QLineEdit" in css.keys()
    assert "QWidget" in css.keys()
    assert "#objectName" in css.keys()
    assert "border" in css.QWidget.keys()
    assert "border" in css.QLineEdit.keys()
    assert "margin" in css["QCheckBox::subcontrol:pseudostate"].keys()
    print css.stylesheet()


def test_style_style(css):
    css.QCheckBox.indicator.unchecked.hover.border = "none"
    css.QCheckBox.indicator.unchecked.hover.color = "green"
    assert css.QCheckBox.indicator.unchecked.hover.style() == \
           "QCheckBox::indicator:unchecked:hover {\n    border: none;\n    color: green;\n}\n"


def test_stylesheet(css):
    css["*"].border = "none"
    css.QFrame.border = "1px solid green"
    css.QFrame.color = "green"
    css.QCheckBox.border = "1px solid green"
    css.QCheckBox.color = "green"
    css.QCheckBox.indicator.background_color = "red"
    css.QCheckBox.indicator.unchecked.border = "none"
    css.QCheckBox.indicator.unchecked.background_color = "rgb(0,20,0)"
    css.QCheckBox.indicator.unchecked.hover.background_color = "purple"
    css.QLineEdit['[echoMode="2"]'].lineedit_password_character = 9679
    css["QCheckBox::indicator:unchecked"].margin = 0

    print
    print css.stylesheet()


def test_empty_style(css):
    css.QCheckBox.indicator.border = "none"
    assert css.QCheckBox.style() == ""


def test_subcontrol_set():
    import qstylizer.style
    qclass_style = qstylizer.style.ClassStyle("QObject")
    with pytest.raises(ValueError):
        qclass_style.text = "test"
    qclass_style.text.color = "red"
    print
    print qclass_style.stylesheet()


def test_pseudostate_set():
    import qstylizer.style
    indicator_style = qstylizer.style.SubControl("indicator")
    with pytest.raises(ValueError):
        indicator_style.pressed = "test"
    indicator_style.pressed.color = "red"
    print
    print indicator_style.stylesheet()


def test_subcontrol_options():
    import qstylizer.setter.subcontrol
    assert 'add-line' in qstylizer.setter.subcontrol.SubControlSetter.get_attr_options()


def test_pseudostate_options():
    import qstylizer.setter.pseudostate
    assert 'minimized' in qstylizer.setter.pseudostate.PseudoStateSetter.get_attr_options()


def test_prop_semicolon(css):
    css.QComboBox.color = "red;"
    assert css.QComboBox.color == "red"


def test_assign_subcontrol(css):
    import qstylizer.style
    indicator = qstylizer.style.SubControl("indicator")
    indicator.background_color = "red"
    indicator.unchecked.border = "none"
    indicator.unchecked.background_color = "rgb(0,20,0)"
    indicator.unchecked.hover.background_color = "purple"

    css.QComboBox.indicator = indicator
    css.QCheckBox.indicator = indicator

    print css.stylesheet()
