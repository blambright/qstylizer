# -*- coding: utf-8 -*-

import re
import copy
import collections

import qstylizer.setter.prop
import qstylizer.setter.subcontrol
import qstylizer.setter.pseudostate


class Style(collections.OrderedDict, qstylizer.setter.prop.PropSetter):
    """Style Object.

    A dictionary containing nested Styles and property:value pairs.

    Example structure::

        <Style>{
            "QCheckBox": <QClassStyle name="QCheckBox">{
                "color": "red",
                "background-color": "black",
                "indicator: <SubControl name="indicator">{
                    "border": "1px solid green",
                    "hover": <PseudoState name="hover">{
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
    def subclass_from_name(cls, name):
        """Determine subclass from string name.

        :param name: name of type string

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

    @classmethod
    def split_identifier(cls, identifier):
        """Split the identifier based on the _split_regex.

        Return a list of each component.
        Example:
            name = "QObject::subcontrol:pseudostate"
            return value = ["QObject", "::subcontrol", ":pseudostate"]

        :param name: String name

        """
        return re.findall(cls._split_regex, identifier)[:-1]

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

    def _find_or_create_value_from_name(self, name):
        """Find or create a value from a string key.

        If the key value already exists, return the value.
        If there is a comma in requested key, return a StyleList object.
        Otherwise create substyles from the style names in the key and return
        the top level substyle or property.

        :param name: The dictionary key

        """
        name = str(name).replace("_", "-")
        value = self._find_value_from_name(name)
        if value is not None:
            return value
        if "," in name:
            style_list = self._create_substyle_list(name)
            return style_list
        return self._create_substyles_from_name(name)

    def _find_value_from_name(self, key):
        """Find value from key.

        Simply return the key's hash value in the ordered dict.

        """
        return self.get(key)

    def _create_substyle_list(self, name):
        """Create a StyleList object and add it to ordered dict.

        :param name: String name

        """
        style_list = StyleList(name=name, parent=self, is_root=False)
        self.__setitem__(name, style_list)
        return style_list

    def _create_substyles_from_name(self, name):
        """Create substyles from name.

        Split the name into individual components based on the _split_regex
        and recursively build the Style hierarchy looping through
        the components.

        If name is "QClass::subcontrol::pseudostate",
        first_key is "QClass" and remaining is "::subcontrol::pseudostate"

        :param name: String to split

        """
        split_names = self.split_identifier(name)
        curr_key = split_names[0]
        first_name = curr_key.replace(":", "")
        remaining = name.split(curr_key, 1)[-1]
        if self._find_value_from_name(first_name) is None:
            self._create_substyle_from_name(curr_key)
        if remaining and remaining != curr_key:
            return self._find_value_from_name(first_name).__getitem__(remaining)
        return self._find_value_from_name(first_name)

    def _create_substyle_from_name(self, name):
        """Create substyle from name.

        Determine subclass from name, create an instance of the subclass,
        then add it to ordered dict.

        :param name: String name

        """
        name_stripped = name.replace(":", "")
        class_ = self.subclass_from_name(name)
        new_style = class_(name=name_stripped, parent=self,
                           is_root=False)
        self.__setitem__(name_stripped, new_style)

    @property
    def identifier(self):
        """Get the identifier.

        Example::

            Object::subcontrol:pseudostate

        """
        if not self._parent:
            return self.name if self.name else ""
        return self._parent.identifier + self.scope_operator + self.name

    @property
    def name(self):
        """Return the name of the Style (eg. "QCheckBox").

        Strip off the scope operator if it exists in name.

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
    def is_root(self):
        return self._is_root

    @property
    def scope_operator(self):
        """Get the scope operator.

        The scope operator is the "::" or ":" that is printed in front
        of the name of the Style in the identifier.

        Subclasses are expected to define the scope operator or else it will
        try to guess it based on its position in the hierarchy.

        """
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

    def style(self):
        """Return the identifier and properties as a single string."""
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
        """Return a stylesheet as string containing the entire hierarchy."""
        stylesheet = self.style()
        for key, value in self.items():
            if isinstance(value, Style):
                stylesheet += value.stylesheet()
        return stylesheet

    def __getitem__(self, key):
        """Override the retrieving of a value from dictionary.

        Find or create style in the key's hash location.

        :param key: The dictionary key

        """
        return self._find_or_create_value_from_name(key)

    def __getattr__(self, name):
        """Override the retrieving of the attribute.

        If attribute starts with an underscore, return the attribute from
        the object's __dict__ otherwise retrieve it from the ordered dict.

        :param name: String name of attribute to retrieve

        """
        if name.startswith("_"):
            return self.__getattribute__(name)
        return self.__getitem__(name)

    def __delattr__(self, name):
        """Override the deleting of an attribute.

        If attribute starts with an underscore, delete the attribute from
        the object's __dict__ otherwise delete it from the ordered dict.

        :param name: String name of attribute to delete

        """
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

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        result.clear()
        for k, v in self.items():
            if isinstance(v, Style):
                v._parent = result
                v._is_root = False
            result.__setitem__(k, copy.deepcopy(v, memo))
        result._parent = self._parent
        return result

    def __repr__(self, *args, **kwargs):
        return self.identifier

    def __str__(self):
        return self.style()


class ClassStyle(Style,
                 qstylizer.setter.subcontrol.SubControlSetter,
                 qstylizer.setter.pseudostate.PseudoStateSetter):
    """The ClassStyle definition.

    Example class style name: "QCheckBox".
    Contains descriptors for all subcontrols and pseudostates.

    """


class ObjectStyle(ClassStyle):
    """The ClassStyle definition.

    Example object style name: "#objectName".
    Inherits from ClassStyle. Only difference is "#" is the scope operator.

    """
    @property
    def scope_operator(self):
        return "#"


class ObjectProperty(Style):
    """The ObjectProperty definition.

    Example object property style name: "[echoMode="2"]".

    """
    @property
    def scope_operator(self):
        return ""


class StyleList(Style):
    """The StyleList definition.

    Example style list name: "QCheckBox, QComboBox".

    """
    @property
    def scope_operator(self):
        return ""

    def __setattr__(self, name, val):
        """Override the setting of an attribute.

        Will loop through all components in name separated by a comma and set the
        property in each of the substyles in the parent Style.

        """
        if name.startswith("_"):
            return super(Style, self).__setattr__(name, val)
        style_names = self.name.split(",")
        for style_name in style_names:
            self._parent.__getitem__(style_name).__setitem__(name, val)
        return None

    @property
    def name(self):
        """Return the name with no spaces."""
        return self._name.replace(" ", "")


class SubControl(Style, qstylizer.setter.pseudostate.PseudoStateSetter):
    """The SubControl definition.

    Example subcontrol name: "::indicator".

    """
    @property
    def scope_operator(self):
        return "::"


class PseudoState(Style):
    """The PseudoState definition.

    Example pseudostate name: ":hover".

    """
    @property
    def scope_operator(self):
        return ":"




