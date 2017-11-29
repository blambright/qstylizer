# coding: utf-8

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
            instance.set_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a SubControlRule, simply add it to the ordered dict.
        Otherwise create a new SubControlRule instance, set its prop_value
        attribute to the value, and add it to the ordered dict.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if isinstance(value, qstylizer.style.SubControlRule):
            value = copy.deepcopy(value)
            value._parent = instance
            instance.set_value(self.name, value)
        else:
            new_style = qstylizer.style.SubControlRule(
                name=self.name,
                parent=instance,
            )
            new_style._prop_value = value
            instance.set_value(self.name, new_style)


class SubControlSetter(qstylizer.setter.StyleRuleSetter):
    """Subcontrol setter.

    Contains descriptors for all known subcontrols.

    """
    _descriptor_cls = SubControlSet

    addLine = _descriptor_cls("add-line")
    addPage = _descriptor_cls("add-page")
    branch = _descriptor_cls("branch")
    chunk = _descriptor_cls("chunk")
    closeButton = _descriptor_cls("close-button")
    corner = _descriptor_cls("corner")
    downArrow = _descriptor_cls("down-arrow")
    downButton = _descriptor_cls("down-button")
    dropDown = _descriptor_cls("drop-down")
    floatButton = _descriptor_cls("float-button")
    groove = _descriptor_cls("groove")
    indicator = _descriptor_cls("indicator")
    handle = _descriptor_cls("handle")
    icon = _descriptor_cls("icon")
    item = _descriptor_cls("item")
    leftArrow = _descriptor_cls("left-arrow")
    leftCorner = _descriptor_cls("left-corner")
    menuArrow = _descriptor_cls("menu-arrow")
    menuButton = _descriptor_cls("menu-button")
    menuIndicator = _descriptor_cls("menu-indicator")
    rightArrow = _descriptor_cls("right-arrow")
    pane = _descriptor_cls("pane")
    rightCorner = _descriptor_cls("right-corner")
    scroller = _descriptor_cls("scroller")
    section = _descriptor_cls("section")
    separator = _descriptor_cls("separator")
    subLine = _descriptor_cls("sub-line")
    subPage = _descriptor_cls("sub-page")
    tab = _descriptor_cls("tab")
    tabBar = _descriptor_cls("tab-bar")
    tear = _descriptor_cls("tear")
    tearoff = _descriptor_cls("tearoff")
    text = _descriptor_cls("text")
    title = _descriptor_cls("title")
    upArrow = _descriptor_cls("up-arrow")
    upButton = _descriptor_cls("up-button")
