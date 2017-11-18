# -*- coding: utf-8 -*-

import copy

import qstylizer.setter


class PseudoPropSet(qstylizer.setter.StyleRuleSet):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.PseudoPropRule(
                name=self.name,
                parent=instance,
            )
            instance._add_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
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

    _descriptor_cls = PseudoPropSet

    left = _descriptor_cls("left")
    right = _descriptor_cls("right")
    top = _descriptor_cls("top")
    bottom = _descriptor_cls("bottom")
