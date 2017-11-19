# coding: utf-8

import tinycss

import qstylizer.style


def parse(stylesheet):
    """Parse a stylesheet using tinycss and return a StyleSheet instance.

    :param stylesheet: A string of an existing stylesheet.

    """
    parsed_stylesheet = tinycss.make_parser().parse_stylesheet(stylesheet)
    css = qstylizer.style.StyleSheet()
    for rule in parsed_stylesheet.rules:
        selector = rule.selector.as_css()
        for declaration in rule.declarations:
            prop = declaration.name
            value = declaration.value.as_css()
            css[selector][prop] = value
    return css
