

import pytest


@pytest.mark.parametrize(
    "selector, expected",
    [
        (
            "QComboBox",
            ["QComboBox"]
        ),
        (
            "QComboBox:pseudostate",
            ["QComboBox", ":pseudostate"]
        ),
        (
            "QComboBox::indicator:pseudostate",
            ["QComboBox", "::indicator", ":pseudostate"]
        ),
        (
            "QWidget[echoMode=2]",
            ["QWidget", "[echoMode=2]"]
        ),
        (
            "QWidget#objectName",
            ["QWidget", "#objectName"]
        ),
        (
            "QWidget QFrame",
            ["QWidget", " QFrame"]
        ),
        (
            "#objectName",
            ["#objectName"]
        ),
        (
            "::pseudostate",
            ["::pseudostate"]
        ),
        (
            "QTreeView::branch:!has-children:adjoins-item",
            ["QTreeView", "::branch", ":!has_children", ":adjoins_item"]
        )
    ],
    ids=[
        "with-single-name",
        "with-pseudostate",
        "with-indicator-and-pseudostate",
        "with-object-property",
        "with-class-and-object",
        "with-child-class",
        "with-object",
        "with-only-pseudostate",
        "with-not-operator-and-dashes"
    ]
)
def test_split_selector(css, selector, expected):
    assert css.split_selector(selector) == expected


@pytest.mark.parametrize(
    "key, expected",
    [
        ("background-color", "background-color"),
        (":checked", "checked"),
        ("background_color", "background-color"),
        (12345, "12345"),
    ],
    ids=[
        "with-normal-key",
        "with-semicolon",
        "with-underscore",
        "with-nonstring",
    ]
)
def test_sanitize_key(css, key, expected):
    assert css._sanitize_key(key) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        ("1px solid #000000", "1px solid #000000"),
        ("1px solid #000000;", "1px solid #000000"),
        (100, 100),
        (u"green;", u"green"),
    ],
    ids=[
        "with-normal-value",
        "with-semicolon",
        "with-nonstring",
        "with-unicode",
    ]
)
def test_sanitize_value(css, value, expected):
    assert css._sanitize_value(value) == expected


@pytest.mark.parametrize(
    "name, "
    "found_value, "
    "expected, "
    "rule_list_call_count, "
    "rules_call_count",
    [
        (
            "QComboBox, QCheckBox",
            None,
            "StyleRuleList",
            1,
            0
        ),
        (
            "QComboBox",
            "Value",
            "Value",
            0,
            0
        ),
        (
            "QComboBox",
            None,
            "Value",
            0,
            1
        ),
    ],
    ids=[
        "with-rule-list",
        "with-existing-class",
        "with-new-class",
    ]
)
def test_find_or_create_rule(
    mocker, css, style_class, name, found_value, expected,
    rule_list_call_count, rules_call_count
):
    mocked_find_rule = mocker.patch.object(
        style_class, "find_rule", return_value=found_value
    )
    mocked_create_rule_list = mocker.patch.object(
        style_class, "create_rule_list", return_value="StyleRuleList"
    )
    mocked_create_rules = mocker.patch.object(
        style_class, "create_rules", return_value=expected
    )
    assert css.find_or_create_rule(name) == expected
    mocked_find_rule.assert_called_once_with(name)
    assert mocked_create_rule_list.call_count == rule_list_call_count
    assert mocked_create_rules.call_count == rules_call_count


def test_find_rule(mocker, style_class, css):
    key = "KEY"
    value = "VALUE"
    mocked_sanitize_key = mocker.patch.object(
        style_class, "_sanitize_key", return_value=key
    )
    mocked_get = mocker.patch.object(
        style_class, "get", return_value=value
    )
    assert css.find_rule(key) == value
    mocked_sanitize_key.assert_called_once_with(key)
    mocked_get.assert_called_once_with(key)


def test_create_rule_list(mocker, style_class, css):
    import qstylizer.style
    style_list = "StyleListInstance"
    name = "test"
    mocker.patch.object(qstylizer.style, "StyleRuleList", return_value=style_list)
    mocked_set_rule = mocker.patch.object(style_class, "set_rule")
    assert css.create_rule_list(name) == style_list
    mocked_set_rule.called_once_with(name, style_list)


@pytest.mark.parametrize(
    "selector, "
    "curr_name, "
    "find_or_create_rule_call_count, ",
    [
        (
            "QComboBox",
            "QComboBox",
            0,
        ),
        (
            "QComboBox::indicator",
            "QComboBox",
            1,
        ),
    ],
    ids=[
        "with-single-style",
        "with-multiple-style",
    ]
)
def test_create_rules(
    mocker, style_class, css, selector, curr_name,
    find_or_create_rule_call_count
):
    mocked_style = mocker.MagicMock()
    mocked_split_selector = mocker.patch.object(
        style_class, "split_selector", return_value=[curr_name]
    )
    mocked_find_rule = mocker.patch.object(
        style_class, "find_rule", return_value=mocked_style
    )
    mocker.patch.object(
        style_class, "create_rule", return_value=mocked_style
    )
    mocker.patch.object(
        style_class, "find_or_create_rule", return_value=mocked_style
    )
    css.create_rules(selector)
    mocked_split_selector.assert_called_once_with(selector)
    mocked_find_rule.assert_called_once_with(curr_name)
    assert mocked_style.find_or_create_rule.call_count == find_or_create_rule_call_count


def test_create_rule(mocker, style_class, css):
    import qstylizer.style
    name = "::indicator"
    style = mocker.MagicMock()
    class_ = mocker.MagicMock(return_value=style)
    mocked_subclass_function = mocker.patch.object(
        qstylizer.style, "rule_class", return_value=class_
    )
    mocked_add_value = mocker.patch.object(
        style_class, "set_rule"
    )
    css.create_rule(name)
    mocked_add_value.assert_called_with(name, style)
    mocked_subclass_function.assert_called_once_with(name)
    class_.assert_called_with(name=name, parent=css)


def test_is_top_level(css):
    pass


def test_style(css):
    pass


def test_to_string_recursive(css):
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


@pytest.mark.parametrize(
    "name, expected",
    [
        ("indicator", "SubControlRule"),
        ("has-children", "PseudoStateRule"),
        ("::subcontrol", "SubControlRule"),
        (":pseudostate", "PseudoStateRule"),
        ("#objectName", "ObjectRule"),
        ("[echoMode=2]", "ObjectPropRule"),
        (" QFrame", "ChildClassRule"),
        ("QObject", "ClassRule")
    ],
    ids=[
        "with-known-subcontrol",
        "with-known-pseudostate",
        "with-subcontrol-scope-op",
        "with-pseudostate-scope-op",
        "with-object",
        "with-object-property",
        "with-child-class",
        "with-known-class",
    ]
)
def test_style_rule_class(mocker, style_class, css, name, expected):
    import qstylizer.style
    assert qstylizer.style.rule_class(name).__name__ == expected

