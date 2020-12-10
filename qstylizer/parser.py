# coding: utf-8

from tinycss.css21 import CSS21Parser

import qstylizer.style


class QSSParser(CSS21Parser):
    def parse_declaration(self, tokens):
        declaration = super(QSSParser, self).parse_declaration(tokens)
        if tokens:
            name = tokens[0].value
            if name.startswith("qproperty-"):
                declaration.name = name
        return declaration


def parse(stylesheet):
    """Parse a stylesheet using tinycss and return a StyleSheet instance.

    :param stylesheet: A string of an existing stylesheet.

    """
    parsed_stylesheet = QSSParser().parse_stylesheet(stylesheet)
    css = qstylizer.style.StyleSheet()
    for rule in parsed_stylesheet.rules:
        selector = rule.selector.as_css()
        for declaration in rule.declarations:
            prop = declaration.name
            value = declaration.value.as_css()
            css[selector][prop] = value
    return css
