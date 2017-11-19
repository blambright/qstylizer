# -*- coding: utf-8 -*-

import copy


class StyleRuleSet(object):
    """StyleRule descriptor."""

    def __init__(self, name):
        """Initialize the StyleRuleSet instance.

        :param name: The attribute name of type string

        """
        self.name = name

    def __get__(self, instance, *args, **kwargs):
        """Get the value from the StyleRule's ordered dict.

        If value doesn't exist, create a new StyleRule instance and add it
        to the StyleRule's ordered dict.

        :param instance: The StyleRule instance

        """
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
        """Set the value in the StyleRule's ordered dict.

        Simply add the value to the ordered dict.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        value = copy.deepcopy(value)
        try:
            value._parent = instance
        except AttributeError:
            pass
        instance._add_value(self.name, value)


class StyleRuleSetter(object):
    """StyleRule Setter.

    Contains functions for getting all known attributes of the StyleRule.

    """
    _descriptor_cls = StyleRuleSet

    @classmethod
    def get_attributes(cls):
        """Get all of the settable attributes of the StyleRule.

        Loop through all base classes to gather all known attributes.
        Returns a dictionary with the attribute name as the key and descriptor
        as the value.

        """
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
        """Get all of the attribute names of the StyleRule.

        Returns a set of all possible dashcase attribute names.

        """
        return set(
            [value.name for value in cls.get_attributes().values()]
        )
