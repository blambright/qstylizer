# -*- coding: utf-8 -*-

import copy

import qstylizer.setter


class SubControlSet(qstylizer.setter.StyleRuleSet):
    """Subcontrol descriptor."""

    def __get__(self, instance, *args, **kwargs):
        """Get the value from the StyleRule's ordered dict.

        If value doesn't exist, create a new SubControlRule instance and add it
        to the StyleRule's ordered dict.

        :param instance: The StyleRule instance

        """
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.SubControlRule(
                name=self.name,
                parent=instance,
            )
            instance._add_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a SubControlRule, simply add it to the ordered dict.
        Otherwise raise a ValueError.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if not isinstance(value, qstylizer.style.SubControlRule):
            raise ValueError("Can only assign a SubControlRule style.")
        value = copy.deepcopy(value)
        value._parent = instance
        instance._add_value(self.name, value)


class SubControlSetter(qstylizer.setter.StyleRuleSetter):
    """Subcontrol setter.

    Contains descriptors for all known subcontrols.

    """
    _descriptor_cls = SubControlSet

    add_line = _descriptor_cls("add-line")
    add_page = _descriptor_cls("add-page")
    branch = _descriptor_cls("branch")
    chunk = _descriptor_cls("chunk")
    close_button = _descriptor_cls("close-button")
    corner = _descriptor_cls("corner")
    down_arrow = _descriptor_cls("down-arrow")
    down_button = _descriptor_cls("down-button")
    drop_down = _descriptor_cls("drop-down")
    float_button = _descriptor_cls("float-button")
    groove = _descriptor_cls("groove")
    indicator = _descriptor_cls("indicator")
    handle = _descriptor_cls("handle")
    icon = _descriptor_cls("icon")
    item = _descriptor_cls("item")
    left_arrow = _descriptor_cls("left-arrow")
    left_corner = _descriptor_cls("left-corner")
    menu_arrow = _descriptor_cls("menu-arrow")
    menu_button = _descriptor_cls("menu-button")
    menu_indicator = _descriptor_cls("menu-indicator")
    right_arrow = _descriptor_cls("right-arrow")
    pane = _descriptor_cls("pane")
    right_corner = _descriptor_cls("right-corner")
    scroller = _descriptor_cls("scroller")
    section = _descriptor_cls("section")
    separator = _descriptor_cls("separator")
    sub_line = _descriptor_cls("sub-line")
    sub_page = _descriptor_cls("sub-page")
    tab = _descriptor_cls("tab")
    tab_bar = _descriptor_cls("tab-bar")
    tear = _descriptor_cls("tear")
    tearoff = _descriptor_cls("tearoff")
    text = _descriptor_cls("text")
    title = _descriptor_cls("title")
    up_arrow = _descriptor_cls("up-arrow")
    up_button = _descriptor_cls("up-button")
