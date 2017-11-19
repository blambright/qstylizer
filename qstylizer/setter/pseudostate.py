# -*- coding: utf-8 -*-

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
            instance._add_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a PseudoStateRule, simply add it to the ordered dict.
        Otherwise raise a ValueError.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if not isinstance(value, qstylizer.style.PseudoStateRule):
            raise ValueError("Can only assign a PseudoStateRule style.")
        value = copy.deepcopy(value)
        value._parent = instance
        instance._add_value(self.name, value)


class PseudoStateSetter(qstylizer.setter.StyleRuleSetter):
    """Pseudostate Setter.

    Contains descriptors for all known pseudostates.

    """
    _descriptor_cls = PseudoStateSet

    active = _descriptor_cls("active")
    adjoins_item = _descriptor_cls("adjoins-item")
    alternate = _descriptor_cls("alternate")
    checked = _descriptor_cls("checked")
    closable = _descriptor_cls("closable")
    closed = _descriptor_cls("closed")
    default = _descriptor_cls("default")
    disabled = _descriptor_cls("disabled")
    edit_focus = _descriptor_cls("edit-focus")
    editable = _descriptor_cls("editable")
    enabled = _descriptor_cls("enabled")
    exclusive = _descriptor_cls("exclusive")
    first = _descriptor_cls("first")
    flat = _descriptor_cls("flat")
    floatable = _descriptor_cls("floatable")
    focus = _descriptor_cls("focus")
    has_children = _descriptor_cls("has-children")
    has_siblings = _descriptor_cls("has-siblings")
    horizontal = _descriptor_cls("horizontal")
    hover = _descriptor_cls("hover")
    indeterminate = _descriptor_cls("indeterminate")
    last = _descriptor_cls("last")
    maximized = _descriptor_cls("maximized")
    middle = _descriptor_cls("middle")
    minimized = _descriptor_cls("minimized")
    movable = _descriptor_cls("movable")
    next_selected = _descriptor_cls("next-selected")
    no_frame = _descriptor_cls("no-frame")
    non_exclusive = _descriptor_cls("non-exclusive")
    off = _descriptor_cls("off")
    on = _descriptor_cls("on")
    only_one = _descriptor_cls("only-one")
    open = _descriptor_cls("open")
    pressed = _descriptor_cls("pressed")
    previous_selected = _descriptor_cls("previous-selected")
    read_only = _descriptor_cls("read-only")
    selected = _descriptor_cls("selected")
    unchecked = _descriptor_cls("unchecked")
    vertical = _descriptor_cls("vertical")
    window = _descriptor_cls("window")
