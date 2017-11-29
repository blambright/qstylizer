# coding: utf-8

import copy

import qstylizer.setter


class PseudoStateSet(qstylizer.setter.StyleRuleSet):
    """Pseudo-state descriptor."""

    def __get__(self, instance, *args, **kwargs):
        """Get the value from the StyleRule's ordered dict.

        If value doesn't exist, create a new PseudoStateRule instance and add it
        to the StyleRule's ordered dict.

        :param instance: The StyleRule instance

        """
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.PseudoStateRule(
                name=self.name,
                parent=instance,
            )
            instance.set_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a PseudoStateRule, simply add it to the ordered dict.
        Otherwise create a new PseudoStateRule instance, set its prop_value
        attribute to the value, and add it to the ordered dict.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if isinstance(value, qstylizer.style.PseudoStateRule):
            value = copy.deepcopy(value)
            value._parent = instance
            instance.set_value(self.name, value)
        else:
            new_style = qstylizer.style.PseudoStateRule(
                name=self.name,
                parent=instance,
            )
            new_style._prop_value = value
            instance.set_value(self.name, new_style)


class PseudoStateSetter(qstylizer.setter.StyleRuleSetter):
    """Pseudostate setter.

    Contains descriptors for all known pseudostates.

    """
    _descriptor_cls = PseudoStateSet

    active = _descriptor_cls("active")
    adjoinsItem = _descriptor_cls("adjoins-item")
    alternate = _descriptor_cls("alternate")
    checked = _descriptor_cls("checked")
    closable = _descriptor_cls("closable")
    closed = _descriptor_cls("closed")
    default = _descriptor_cls("default")
    disabled = _descriptor_cls("disabled")
    editFocus = _descriptor_cls("edit-focus")
    editable = _descriptor_cls("editable")
    enabled = _descriptor_cls("enabled")
    exclusive = _descriptor_cls("exclusive")
    first = _descriptor_cls("first")
    flat = _descriptor_cls("flat")
    floatable = _descriptor_cls("floatable")
    focus = _descriptor_cls("focus")
    hasChildren = _descriptor_cls("has-children")
    hasSiblings = _descriptor_cls("has-siblings")
    horizontal = _descriptor_cls("horizontal")
    hover = _descriptor_cls("hover")
    indeterminate = _descriptor_cls("indeterminate")
    last = _descriptor_cls("last")
    maximized = _descriptor_cls("maximized")
    middle = _descriptor_cls("middle")
    minimized = _descriptor_cls("minimized")
    movable = _descriptor_cls("movable")
    nextSelected = _descriptor_cls("next-selected")
    noFrame = _descriptor_cls("no-frame")
    nonExclusive = _descriptor_cls("non-exclusive")
    off = _descriptor_cls("off")
    on = _descriptor_cls("on")
    onlyOne = _descriptor_cls("only-one")
    open = _descriptor_cls("open")
    pressed = _descriptor_cls("pressed")
    previous_selected = _descriptor_cls("previous-selected")
    readOnly = _descriptor_cls("read-only")
    selected = _descriptor_cls("selected")
    unchecked = _descriptor_cls("unchecked")
    vertical = _descriptor_cls("vertical")
    window = _descriptor_cls("window")
