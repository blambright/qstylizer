

import pytest
import mock


@pytest.mark.parametrize(
    "name, expected_subclass",
    [
        ("indicator", "SubControl"),
        ("has-children", "PseudoState"),
        ("::subcontrol", "SubControl"),
        (":pseudostate", "PseudoState"),
        ("#objectName", "ObjectStyle"),
        ("[echoMode=2]", "ObjectProperty"),
        (" QFrame", "ChildClassStyle"),
        ("QObject", "ClassStyle")
    ]
)
def test_subclass_from_name(css, name, expected_subclass):
    type(css)._subcontrols = mock.PropertyMock(
        return_value={"indicator", "add_line", "branch"}
    )
    type(css)._pseudostates = mock.PropertyMock(
        return_value={"alternate", "has-children", "branch"}
    )
    assert css.subclass_from_name(name).__name__ == expected_subclass


@pytest.mark.parametrize(
    "identifier, expected_result",
    [
        ("QComboBox", ["QComboBox"]),
        ("QComboBox:pseudostate", ["QComboBox", ":pseudostate"]),
        ("QComboBox::indicator:pseudostate", ["QComboBox", "::indicator", ":pseudostate"]),
        ("QWidget[echoMode=2]", ["QWidget", "[echoMode=2]"]),
        ("QWidget#objectName", ["QWidget", "#objectName"]),
        ("QWidget QFrame", ["QWidget", " QFrame"]),
        ("#objectName", ["#objectName"]),
        ("::pseudostate", ["::pseudostate"]),
    ]
)
def test_split_identifier(css, identifier, expected_result):
    assert css.split_identifier(identifier) == expected_result


@pytest.mark.parametrize(
    "name, found_value, expected_result",
    [
        ("QComboBox, QCheckBox", None, "StyleList"),
        ("QComboBox", "Value", "Value"),
        ("QComboBox", None, "Value"),
    ]
)
def test_find_or_create_value_from_name(
    mocker, css, name, found_value, expected_result
):
    mocked_create_substyle_list = mocker.patch.object(
        css, "_create_substyle_list", return_value="StyleList"
    )
    mocked_create_substyles_from_name = mocker.patch.object(
        css, "_create_substyles_from_name", return_value=expected_result
    )
    mocked_find_value_from_name = mocker.patch.object(
        css, "_find_value_from_name", return_value=found_value
    )
    assert css._find_or_create_value_from_name(name) == expected_result
    mocked_find_value_from_name.assert_called_once_with(name)
    if "," in name:
        mocked_create_substyle_list.assert_called_once_with(name)
    elif not found_value:
        mocked_create_substyles_from_name.assert_called_once_with(name)


def test_find_value_from_name(mocker, css):
    # expected_result = "Value"
    # name = "Test"
    # mocked_function = mocker.patch.object(
    #     css, "get", return_value=expected_result
    # )
    # # print css.get
    # # assert css._find_value_from_name(name) == expected_result
    # mocked_function.assert_called_once_with(name)
    pass


def test_create_substyle_list(css):
    pass


# @pytest.mark.parametrize(
#     "name, curr_key, first, value, remaining", [
#         ("QComboBox", "QComboBox", "QComboBox", ""),
#         ("QComboBox::indicator", "QComboBox", "QComboBox", ""),
#     ]
# )
# def test_create_substyles_from_name(
#     mocker, css, name, curr_key, first, value, remaining
# ):
#     mocked_find_value_from_name = mocker.patch.object(
#         css, "_find_value_from_name"
#     )
#     mocked_getitem = mocker.patch.object(
#         mocked_find_value_from_name, "__getitem__"
#     )
#     mocked_create_substyle_from_name = mocker.patch.object(
#         css, "_create_substyle_from_name"
#     )
#     css._create_substyles_from_name(name)
#     mocked_find_value_from_name.assert_called_with(first)
#     # mocked_create_substyle_from_name.assert_called_with(curr_key)


def test_create_substyle_from_name(css):
    pass


def test_identifier(css):
    pass


def test_name(css):
    pass


def test_parent(css):
    pass


def test_is_root(css):
    pass


def test_scope_operator(css):
    pass


def test_is_top_level(css):
    pass


def test_style(css):
    pass


def test_stylesheet(css):
    pass


def test_getitem(css):
    pass


def test_getattr(css):
    pass


def test_delattr(css):
    pass


def test_setattr(css):
    pass


def test_deepcopy(css):
    pass


def test_repr(css):
    pass


def test_str(css):
    pass




