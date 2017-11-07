# -*- coding: utf-8 -*-

import qstylizer.setter

_property_values = {
    "active",
    "alternate-base",
    "always",
    "auto",
    "base",
    "bold",
    "bottom",
    "bright-text",
    "button",
    "button-text",
    "center",
    "circle",
    "dark",
    "dashed",
    "decimal",
    "disabled",
    "disc",
    "dot-dash",
    "dot-dot-dash",
    "dotted",
    "double",
    "groove",
    "highlight",
    "highlighted-text",
    "inset",
    "italic",
    "large",
    "left",
    "light",
    "line-through",
    "link",
    "link-visited",
    "lower-alpha",
    "lower-roman",
    "lowercase",
    "medium",
    "mid",
    "middle",
    "midlight",
    "native",
    "none",
    "normal",
    "nowrap",
    "oblique",
    "off",
    "on",
    "outset",
    "overline",
    "pre",
    "pre-wrap",
    "ridge",
    "right",
    "selected",
    "shadow",
    "small",
    "small-caps",
    "solid",
    "square",
    "sub",
    "super",
    "text",
    "top",
    "transparent",
    "underline",
    "upper-alpha",
    "upper-roman",
    "uppercase",
    "wave",
    "window",
    "window-text",
    "x-large",
    "xx-large",
}

_origins = {
    "border",
    "content",
    "margin",
    "padding",
}

_repeats = {
    "no-repeat",
    "repeat-x",
    "repeat-xy",
    "repeat-y",
}

_tile_modes = {
    "repeat",
    "round",
    "stretch",
}

_positions = {
    "absolute",
    "fixed",
    "relative",
    "static",
}

_attachments = {
    "fixed",
    "scroll",
}

_style_features = {
    "background-color",
    "background-gradient",
    "none",
}


def get_origins():
    return _origins


def get_repeats():
    return _repeats


def get_tile_modes():
    return _tile_modes


def get_positions():
    return _positions


def get_attachments():
    return _attachments


def get_style_features():
    return _style_features


def get_property_values():
    return _property_values


class PropSet(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.Style)
        return instance.__getitem__(self.name)

    def __set__(self, instance, value):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.Style)
        try:
            value = value.replace(";", "")
        except AttributeError:
            pass
        instance.__setitem__(self.name, value)


class PropSetter(qstylizer.setter.Setter):

    _descriptor_cls = PropSet

    qt_background_role = _descriptor_cls("-qt-background-role")
    qt_block_indent = _descriptor_cls("-qt-block-indent")
    qt_line_height_type = _descriptor_cls("-qt-line-height-type")
    qt_list_indent = _descriptor_cls("-qt-list-indent")
    qt_list_number_prefix = _descriptor_cls("-qt-list-number-prefix")
    qt_list_number_suffix = _descriptor_cls("-qt-list-number-suffix")
    qt_paragraph_type = _descriptor_cls("-qt-paragraph-type")
    qt_style_features = _descriptor_cls("-qt-style-features")
    qt_table_type = _descriptor_cls("-qt-table-type")
    qt_user_state = _descriptor_cls("-qt-user-state")
    alternate_background_color = _descriptor_cls("alternate-background-color")
    background = _descriptor_cls("background")
    background_attachment = _descriptor_cls("background-attachment")
    background_clip = _descriptor_cls("background-clip")
    background_color = _descriptor_cls("background-color")
    background_image = _descriptor_cls("background-image")
    background_origin = _descriptor_cls("background-origin")
    background_position = _descriptor_cls("background-position")
    background_repeat = _descriptor_cls("background-repeat")
    border = _descriptor_cls("border")
    border_bottom = _descriptor_cls("border-bottom")
    border_bottom_color = _descriptor_cls("border-bottom-color")
    border_bottom_left_radius = _descriptor_cls("border-bottom-left-radius")
    border_bottom_right_radius = _descriptor_cls("border-bottom-right-radius")
    border_bottom_style = _descriptor_cls("border-bottom-style")
    border_bottom_width = _descriptor_cls("border-bottom-width")
    border_color = _descriptor_cls("border-color")
    border_image = _descriptor_cls("border-image")
    border_left = _descriptor_cls("border-left")
    border_left_color = _descriptor_cls("border-left-color")
    border_left_style = _descriptor_cls("border-left-style")
    border_left_width = _descriptor_cls("border-left-width")
    border_radius = _descriptor_cls("border-radius")
    border_right = _descriptor_cls("border-right")
    border_right_color = _descriptor_cls("border-right-color")
    border_right_style = _descriptor_cls("border-right-style")
    border_right_width = _descriptor_cls("border-right-width")
    border_style = _descriptor_cls("border-style")
    border_top = _descriptor_cls("border-top")
    border_top_color = _descriptor_cls("border-top-color")
    border_top_left_radius = _descriptor_cls("border-top-left-radius")
    border_top_right_radius = _descriptor_cls("border-top-right-radius")
    border_top_style = _descriptor_cls("border-top-style")
    border_top_width = _descriptor_cls("border-top-width")
    border_width = _descriptor_cls("border-width")
    bottom = _descriptor_cls("bottom")
    color = _descriptor_cls("color")
    float = _descriptor_cls("float")
    font = _descriptor_cls("font")
    font_family = _descriptor_cls("font-family")
    font_size = _descriptor_cls("font-size")
    font_style = _descriptor_cls("font-style")
    font_variant = _descriptor_cls("font-variant")
    font_weight = _descriptor_cls("font-weight")
    height = _descriptor_cls("height")
    image = _descriptor_cls("image")
    image_position = _descriptor_cls("image-position")
    left = _descriptor_cls("left")
    line_height = _descriptor_cls("line-height")
    list_style = _descriptor_cls("list-style")
    list_style_type = _descriptor_cls("list-style-type")
    margin = _descriptor_cls("margin")
    margin_bottom = _descriptor_cls("margin-bottom")
    margin_left = _descriptor_cls("margin-left")
    margin_right = _descriptor_cls("margin-right")
    margin_top = _descriptor_cls("margin-top")
    max_height = _descriptor_cls("max-height")
    max_width = _descriptor_cls("max-width")
    min_height = _descriptor_cls("min-height")
    min_width = _descriptor_cls("min-width")
    outline = _descriptor_cls("outline")
    outline_bottom_left_radius = _descriptor_cls("outline-bottom-left-radius")
    outline_bottom_right_radius = _descriptor_cls("outline-bottom-right-radius")
    outline_color = _descriptor_cls("outline-color")
    outline_offset = _descriptor_cls("outline-offset")
    outline_radius = _descriptor_cls("outline-radius")
    outline_style = _descriptor_cls("outline-style")
    outline_top_left_radius = _descriptor_cls("outline-top-left-radius")
    outline_top_right_radius = _descriptor_cls("outline-top-right-radius")
    outline_width = _descriptor_cls("outline-width")
    padding = _descriptor_cls("padding")
    padding_bottom = _descriptor_cls("padding-bottom")
    padding_left = _descriptor_cls("padding-left")
    padding_right = _descriptor_cls("padding-right")
    padding_top = _descriptor_cls("padding-top")
    page_break_after = _descriptor_cls("page-break-after")
    page_break_before = _descriptor_cls("page-break-before")
    position = _descriptor_cls("position")
    right = _descriptor_cls("right")
    selection_background_color = _descriptor_cls("selection-background-color")
    selection_color = _descriptor_cls("selection-color")
    spacing = _descriptor_cls("spacing")
    subcontrol_origin = _descriptor_cls("subcontrol-origin")
    subcontrol_position = _descriptor_cls("subcontrol-position")
    text_align = _descriptor_cls("text-align")
    text_decoration = _descriptor_cls("text-decoration")
    text_indent = _descriptor_cls("text-indent")
    text_transform = _descriptor_cls("text-transform")
    text_underline_style = _descriptor_cls("text-underline-style")
    top = _descriptor_cls("top")
    vertical_align = _descriptor_cls("vertical-align")
    white_space = _descriptor_cls("white-space")
    width = _descriptor_cls("width")
