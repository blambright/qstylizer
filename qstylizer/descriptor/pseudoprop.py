# coding: utf-8

import copy

import qstylizer.descriptor


class PseudoPropDescriptor(qstylizer.descriptor.StyleRuleDescriptor):
    """Pseudo-property descriptor."""


class PseudoPropSetter(qstylizer.descriptor.StyleRuleSetter):
    """Pseudo-property setter.

    Contains descriptors for all known pseudo-properties.

    """
    _descriptor_cls = PseudoPropDescriptor

    left = _descriptor_cls("left")
    right = _descriptor_cls("right")
    top = _descriptor_cls("top")
    bottom = _descriptor_cls("bottom")
