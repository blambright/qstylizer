# coding: utf-8

import tinycss2

import qstylizer.style


def _strip_whitespace_recursive(value):
    for i, v in enumerate(value):
        if isinstance(v, list):
            value[i].value = _strip_whitespace_recursive(v)
        else:
            try:
                value[i].value = v.value.strip()
            except AttributeError:
                pass
    return value


def parse(stylesheet):
    """Parse a stylesheet using tinycss2 and return a StyleSheet instance.

    :param stylesheet: A string of an existing stylesheet.

    """
    parsed_stylesheet = tinycss2.parse_stylesheet(
        stylesheet, skip_comments=True, skip_whitespace=True
    )
    css = qstylizer.style.StyleSheet()
    for node in parsed_stylesheet:
        if node.type == "error":
            raise ValueError("Cannot parse Stylesheet: " + node.message)
        selector = tinycss2.serialize(_strip_whitespace_recursive(node.prelude))
        declaration_list = tinycss2.parse_declaration_list(
            node.content, skip_comments=True, skip_whitespace=True
        )
        for declaration in declaration_list:
            if declaration.type == "declaration":
                prop = declaration.name.strip()
                v = _strip_whitespace_recursive(declaration.value)
                value = tinycss2.serialize(v)
                css[selector][prop] = value
    return css
