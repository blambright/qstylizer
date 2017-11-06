
import re
import collections

import qstylizer.setter.prop
import qstylizer.setter.subcontrol
import qstylizer.setter.pseudostate


class Style(collections.OrderedDict, qstylizer.setter.prop.PropSetter):
    """Style Object.

    A dictionary containing nested Styles and property:value pairs.

    Example structure::

        <Style>{
            <QClassStyle name="QCheckBox">: {
                "color": "red",
                "background-color": "black",
                <SubControl name="indicator">: {
                    "border": "1px solid green",
                    <PseudoState name="hover">: {
                        "background-color": "green",
                    }
                }
            }
        }

    """
    _split_regex = "\[[A-Za-z0-9='\"]+\]|\W*\w*"
    _properties = qstylizer.setter.prop.PropSetter.get_attr_options()
    _subcontrols = qstylizer.setter.subcontrol.SubControlSetter.get_attr_options()
    _pseudostates = qstylizer.setter.pseudostate.PseudoStateSetter.get_attr_options()

    @classmethod
    def _subclass_from_name(cls, name):
        """Determine subclass from string name.

        :param name: name of type string
        :return: Style subclass

        """
        class_ = ClassStyle
        if name.startswith("::") or name in cls._subcontrols:
            class_ = SubControl
        elif name.startswith(":") or name in cls._pseudostates:
            class_ = PseudoState
        elif name.startswith("#"):
            class_ = ObjectStyle
        elif "=" in name:
            class_ = ObjectProperty
        return class_

    def __init__(self, name=None, parent=None, is_root=True):
        """Initialize the style dictionary.

        :param name: The name of the Style
        :param parent:  The parent Style
        :param is_root: Is root of stylesheet hierarchy

        """
        super(Style, self).__init__()

        self._name = name
        self._parent = parent
        self._children = {}
        self._is_root = is_root
        self._attributes = self.get_attributes()

    def __getitem__(self, key):
        """Override the retrieving of a value from dictionary.

        Find or create style in the key's hash location.
        Split the requested key into individual components based on the _split_regex
        and recursively build the hierarchy looping through the components.

        If name is "QClass::subcontrol::pseudostate":
            first_key is "QClass"
            remaining is "::subcontrol::pseudostate"

        :param key: The dictionary key

        """
        return self._find_or_create_value_from_key(key)

    def _find_or_create_value_from_key(self, key):
        key = key.replace("_", "-")
        value = self._find_value_from_key(key)
        if value is not None:
            return value
        if "," in key:
            style_list = self._create_substyle_list(key)
            return style_list
        return self._create_substyles_from_names(key)

    def _find_value_from_key(self, key):
        return self.get(key)

    def _create_substyle_list(self, key):
        style_list = StyleList(name=key, parent=self, is_root=False)
        self.__setitem__(key, style_list)
        return style_list

    def _create_substyles_from_names(self, names):
        split_names = re.findall(self._split_regex, names)[:-1]
        curr_key = split_names[0]
        name = curr_key.replace(":", "")
        remaining = names.split(curr_key, 1)[-1]
        if self.get(name) is None:
            self._create_substyle_from_name(curr_key)
        if remaining and remaining != curr_key:
            return self._find_value_from_key(name).__getitem__(remaining)
        return self._find_value_from_key(name)

    def _create_substyle_from_name(self, name):
        name_stripped = name.replace(":", "")
        class_ = self._subclass_from_name(name)
        new_style = class_(name=name_stripped, parent=self,
                           is_root=False)
        self.__setitem__(name_stripped, new_style)

    def __getattr__(self, name):
        if name.startswith("_"):
            return self.__getattribute__(name)
        return self.__getitem__(name)

    def __delattr__(self, name):
        if name in self.__dict__:
            return super(Style, self).__delattr__(name)
        return self.__delitem__(name)

    def __setattr__(self, name, val):
        if name.startswith("_"):
            return super(Style, self).__setattr__(name, val)
        elif name in self._attributes:
            return self._attributes[name].__set__(self, val)
        name = name.replace('_', '-')
        return self.__setitem__(name, val)



    @property
    def identifier(self):
        """Get the identifier.

        Example:
            Object::subcontrol::pseudostate

        """
        if not self._parent:
            return self.name if self.name else ""
        return self._parent.identifier + self.scope_operator + self.name

    @property
    def name(self):
        """Return the name of the Style (eg. "QCheckBox").

        Strip off the scope operator if exists in name.

        """
        if (self._name and self.scope_operator and
           self._name.startswith(self.scope_operator)):
            return self._name.split(self.scope_operator, 1)[-1]
        return self._name

    @name.setter
    def name(self, name):
        self._name = name.replace("_", "-").replace(":", "")

    @property
    def parent(self):
        return self._parent

    @property
    def scope_operator(self):
        if self.is_top_level():
            return ""
        elif self.is_leaf():
            return ":"
        return "::"

    def is_leaf(self):
        """Determine if style is a leaf.

        Style is a leaf if its dictionary values contain no Styles (only properties).

        """
        return not [style for style in self.values() if isinstance(style, Style)]

    def is_top_level(self):
        return self._parent.is_root

    @property
    def is_root(self):
        return self._is_root

    def style(self):
        properties = ""
        sheet = ""
        identifier = self.identifier
        for key, value in self.items():
            if not isinstance(value, Style):
                properties += "    {}: {};\n".format(key, value)
        if properties:
            sheet = "{identifier} {{\n{properties}}}\n".format(**locals())
        return sheet

    def stylesheet(self):
        stylesheet = self.style()
        for key, value in self.items():
            if isinstance(value, Style):
                stylesheet += value.stylesheet()
        return stylesheet

    def __repr__(self, *args, **kwargs):
        return self.identifier

    def __str__(self):
        return self.style()


class ClassStyle(Style,
                 qstylizer.setter.subcontrol.SubControlSetter,
                 qstylizer.setter.pseudostate.PseudoStateSetter):
    pass


class ObjectStyle(ClassStyle):

    @property
    def scope_operator(self):
        return "#"


class ObjectProperty(Style):

    @property
    def scope_operator(self):
        return ""


class StyleList(Style):

    @property
    def scope_operator(self):
        return ""

    def __setattr__(self, name, val):
        if name.startswith("_"):
            return super(Style, self).__setattr__(name, val)
        style_names = self.name.split(",")
        for style_name in style_names:
            self._parent.__getitem__(style_name).__setitem__(name, val)
        return None

    @property
    def name(self):
        name = self._name
        return name.replace(" ", "")


class SubControl(Style, qstylizer.setter.pseudostate.PseudoStateSetter):

    @property
    def scope_operator(self):
        return "::"


class PseudoState(Style):

    @property
    def scope_operator(self):
        return ":"




