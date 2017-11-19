# coding: utf-8

import copy

import qstylizer.setter


class PseudoPropSet(qstylizer.setter.StyleRuleSet):
    """Pseudo-property descriptor."""

    def __get__(self, instance, *args, **kwargs):
        """Get the value from the StyleRule's ordered dict.

        If value doesn't exist, create a new PseudoPropRule instance and add it
        to the StyleRule's ordered dict.

        :param instance: The StyleRule instance

        """
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            style_rule = qstylizer.style.PseudoPropRule(
                name=self.name,
                parent=instance,
            )
            instance._add_value(self.name, style_rule)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a PseudoPropRule, simply add it to the ordered dict.
        Otherwise create a new PseudoPropRule instance, set its prop_value
        attribute to the value, and add it to the ordered dict.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if isinstance(value, qstylizer.style.PseudoPropRule):
            value = copy.deepcopy(value)
            value._parent = instance
            instance._add_value(self.name, value)
        else:
            new_style = qstylizer.style.PseudoPropRule(
                name=self.name,
                parent=instance,
            )
            new_style._prop_value = value
            instance._add_value(self.name, new_style)


class PseudoPropSetter(qstylizer.setter.StyleRuleSetter):
    """Pseudo-property setter.

    Contains descriptors for all known pseudo-properties.

    """
    _descriptor_cls = PseudoPropSet

    left = _descriptor_cls("left")
    right = _descriptor_cls("right")
    top = _descriptor_cls("top")
    bottom = _descriptor_cls("bottom")
