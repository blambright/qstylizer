# -*- coding: utf-8 -*-

import copy

import qstylizer.setter


class PseudoStateSet(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.Style)
        if instance.get(self.name) is None:
            new_style = qstylizer.style.PseudoState(
                name=self.name,
                parent=instance,
                is_root=False
            )
            instance.add_value(self.name, new_style)
        return instance.get(self.name)

    def __set__(self, instance, value):
        import qstylizer.style
        if not isinstance(value, qstylizer.style.PseudoState):
            raise ValueError("Can only assign a PseudoState style.")
        value = copy.deepcopy(value)
        value._is_root = False
        value._parent = instance
        instance.add_value(self.name, value)


class PseudoStateSetter(qstylizer.setter.Setter):

    _descriptor_cls = PseudoStateSet

    active = _descriptor_cls("active")
    adjoins_item = _descriptor_cls("adjoins-item")
    alternate = _descriptor_cls("alternate")
    bottom = _descriptor_cls("bottom")
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
    left = _descriptor_cls("left")
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
    right = _descriptor_cls("right")
    selected = _descriptor_cls("selected")
    top = _descriptor_cls("top")
    unchecked = _descriptor_cls("unchecked")
    vertical = _descriptor_cls("vertical")
    window = _descriptor_cls("window")
