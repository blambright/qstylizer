# coding: utf-8

import copy

import qstylizer.setter


class PseudoPropSet(qstylizer.setter.StyleRuleSet):
    """Pseudo-property descriptor."""


class PseudoPropSetter(qstylizer.setter.StyleRuleSetter):
    """Pseudo-property setter.

    Contains descriptors for all known pseudo-properties.

    """
    _descriptor_cls = PseudoPropSet

    left = _descriptor_cls("left")
    right = _descriptor_cls("right")
    top = _descriptor_cls("top")
    bottom = _descriptor_cls("bottom")
