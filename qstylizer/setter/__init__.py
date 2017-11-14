# -*- coding: utf-8 -*-

import copy


class StyleRuleSet(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.StyleRule(
                name=self.name,
                parent=instance,
            )
            instance._add_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        value = copy.deepcopy(value)
        try:
            value._parent = instance
        except AttributeError:
            pass
        instance._add_value(self.name, value)


class StyleRuleSetter(object):

    _descriptor_cls = StyleRuleSet

    left = _descriptor_cls("left")
    right = _descriptor_cls("right")
    top = _descriptor_cls("top")
    bottom = _descriptor_cls("bottom")

    @classmethod
    def get_attributes(cls):
        attributes = {}
        for class_ in cls.__bases__:
            if not issubclass(class_, StyleRuleSetter):
                continue
            attributes.update({
                key: value for key, value in class_.__dict__.items()
                if isinstance(value, class_._descriptor_cls)
            })
            attributes.update(class_.get_attributes())
        attributes.update({
            key: value for key, value in cls.__dict__.items()
            if isinstance(value, cls._descriptor_cls)
        })
        return attributes

    @classmethod
    def get_attr_options(cls):
        return set(
            [value.name for value in cls.get_attributes().values()]
        )
