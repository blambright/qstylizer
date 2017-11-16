# -*- coding: utf-8 -*-

import re
import copy
import collections

import qstylizer.setter.prop
import qstylizer.setter.subcontrol
import qstylizer.setter.pseudostate
import qstylizer.setter.qclass


class StyleRule(collections.OrderedDict, qstylizer.setter.prop.PropSetter):
    """StyleRule Object.

    A dictionary containing nested Styles and property:value pairs.

    Example structure:

    .. code-block:: xml

        <ClassRule name="QCheckBox" dict={
            "color": "red",
            "background-color": "black",
            "indicator: <SubControlRule name="indicator" dict={
                "border": "1px solid green",
                "hover": <PseudoStateRule name="hover" dict={
                    "background-color": "green",
                    "border": "0px transparent black"
                } />
            } />
        } />

    Output format::

        <selector> {
            <property>: <value>;
            <property>: <value>;
            ...
        }

    Stylesheet output::

        QCheckBox {
            color: red;
            background-color: black;
        }
        QCheckBox::indicator {
            border: 1px solid green;
        }
        QCheckBox::indicator:hover {
            background-color: green;
            border: 0px transparent black;
        }

    """
    _split_regex = "\[[A-Za-z0-9='\"]+\]|\W*\w*"
    qproperties = qstylizer.setter.prop.PropSetter.get_attr_options()
    qsubcontrols = qstylizer.setter.subcontrol.SubControlSetter.get_attr_options()
    qpseudostates = qstylizer.setter.pseudostate.PseudoStateSetter.get_attr_options()
    qclasses = qstylizer.setter.qclass.ClassStyleSetter.get_attr_options()

    @classmethod
    def subclass(cls, name):
        """Determine StyleRule subclass from string name.

        :param name: name of type string

        """
        name = name.replace("not_", "").replace("!", "")
        class_ = StyleRule
        if name.startswith("::") or name in cls.qsubcontrols:
            class_ = SubControlRule
        elif name.startswith(":") or name in cls.qpseudostates:
            class_ = PseudoStateRule
        elif name.startswith("#"):
            class_ = ObjectRule
        elif name.startswith(" "):
            class_ = ChildClassRule
        elif name in cls.qclasses or name.startswith("Q"):
            class_ = ClassRule
        elif "=" in name:
            class_ = ObjectPropRule
        return class_

    @classmethod
    def split_selector(cls, selector):
        """Split the selector based on the _split_regex.

        Return a list of each component.
        Example::

            name = "QObject::subcontrol:pseudostate"
            return value = ["QObject", "::subcontrol", ":pseudostate"]

        :param name: String name

        """
        selector = selector.replace("-", "_")
        return re.findall(cls._split_regex, selector)[:-1]

    def __init__(self, name=None, parent=None):
        """Initialize the StyleRule dictionary.

        .. note:: All public variables will be put into ordered dictionary.

        :param name: The name of the StyleRule
        :param parent:  The parent StyleRule

        """
        super(StyleRule, self).__init__()

        self._name = self._sanitize_key(name) if name else None
        self._parent = parent
        self._attributes = self.get_attributes()
        self._attr_options = self.get_attr_options()

    @staticmethod
    def _sanitize_key(key):
        """Strip the key of colons and replace underscores with dashes.

        :param key: A string variable

        """
        return (
            str(key)
            .replace("not_", "!")
            .replace(":", "")
            .replace("_", "-")
        )

    @staticmethod
    def _sanitize_value(value):
        """Strip the value of any semi-colons.

        :param value: A value of any type

        """
        if type(value) in [str, unicode]:
            return value.replace(";", "")
        return value

    def find_or_create_value(self, name):
        """Find or create a value from a string key.

        If the key value already exists, return the value.
        If there is a comma in requested key, return a StyleRuleList object.
        Otherwise create substyles from the style names in the key and return
        the top level substyle or property.

        :param name: The dictionary key

        """
        value = self.find_value(name)
        if value is not None:
            return value
        if "," in name:
            style_list = self.create_substyle_list(name)
            return style_list
        return self.create_substyles(name)

    def find_value(self, key):
        """Find value from key.

        Return the sanitized key's hash value in the ordered dict.

        """
        key = self._sanitize_key(key)
        return self.get(key)

    def create_substyle_list(self, name):
        """Create a StyleRuleList object and add it to ordered dict.

        :param name: String name

        """
        style_list = StyleRuleList(name=name, parent=self)
        self._add_value(name, style_list)
        return style_list

    def create_substyles(self, selector):
        """Create substyles from selector.

        Split the selector into individual components based on the _split_regex
        and recursively build the StyleRule hierarchy looping through
        the components.

        If selector is "QClass::subcontrol::pseudostate",
        first_key is "QClass" and remaining is "::subcontrol::pseudostate"

        :param name: String to split

        """
        curr_name = self.split_selector(selector)[0]
        remaining = selector.split(curr_name, 1)[-1].replace("-", "_")
        style = self.find_value(curr_name)
        if style is None:
            style = self.create_substyle(curr_name)
        if remaining and remaining != curr_name:
            return style.find_or_create_value(remaining)
        return style

    def create_substyle(self, name):
        """Create substyle from name.

        Determine subclass from name, create an instance of the subclass,
        then add it to ordered dict.

        :param name: String name

        """
        class_ = self.subclass(name)
        style = class_(name=name, parent=self)
        self._add_value(name, style)
        return style

    def _add_value(self, key, value, **kwargs):
        """Add item to ordered dictionary."""
        key = self._sanitize_key(key)
        value = self._sanitize_value(value)
        super(StyleRule, self).__setitem__(key, value, **kwargs)
        return self.find_value(key)

    @property
    def selector(self):
        """Get the selector.

        Example::

            Object::subcontrol:pseudostate

        """
        if not self._parent:
            return self.name if self.name else ""
        return self._parent.selector + self.scope_operator + self.name

    @property
    def name(self):
        """Return the name of the StyleRule (eg. "QCheckBox").

        Strip off the scope operator if it exists in name.

        """
        if (self._name and self.scope_operator and
           self._name.startswith(self.scope_operator)):
            return self._name.split(self.scope_operator, 1)[-1]
        return self._name

    @name.setter
    def name(self, name):
        self._name = self._sanitize_key(name)

    @property
    def parent(self):
        return self._parent

    @property
    def scope_operator(self):
        """Get the scope operator.

        The scope operator is the "::" or ":" that is printed in front
        of the name of the StyleRule in the selector.

        Subclasses are expected to define the scope operator or else it will
        try to guess it based on its position in the hierarchy.

        """
        if self.is_top_level():
            return ""
        elif self.is_leaf():
            return ":"
        return "::"

    def is_leaf(self):
        """Determine if StyleRule is a leaf.

        StyleRule is a leaf if its dictionary values
        contain no Styles (only properties).

        """
        for value in self.values():
            if isinstance(value, StyleRule):
                return False
        return True

    def is_top_level(self):
        """Determine if StyleRule is top level.

        StyleRule is top level if its parent is of the StyleSheet class.

        """
        return isinstance(self._parent, StyleSheet)

    def _stylesheet(self):
        """Return the stylesheet.

        Loop through all of the substyles and generate a stylesheet string.

        """
        stylesheet = self.to_string(cascade=False)
        for key, value in self.items():
            if isinstance(value, StyleRule):
                stylesheet += value.to_string(cascade=True)
        return stylesheet

    def to_string(self, cascade=False):
        """Convert to a single string in css format.

        :param cascade: If True, output all of the sub-styles in hierarchy.

        """
        if cascade:
            return self._stylesheet()
        style_format = "{selector} {{\n{properties}}}\n"
        prop_format = "    {}: {};\n"
        properties = ""
        sheet = ""
        selector = self.selector
        for key, value in self.items():
            if not isinstance(value, StyleRule):
                properties += prop_format.format(key, value)
        if properties:
            sheet = style_format.format(**locals())
        return sheet

    def __getitem__(self, key):
        """Override the retrieving of a value from dictionary.

        Find or create style in the key's hash location.

        :param key: The dictionary key

        """
        return self.find_or_create_value(key)

    def __getattr__(self, name):
        """Override the retrieving of an attribute.

        If attribute starts with an underscore, return the attribute from
        the object's __dict__ otherwise retrieve or create it in the ordered dict.

        :param name: String name of attribute to retrieve

        """
        if name.startswith("_"):
            return self.__getattribute__(name)
        return self.find_or_create_value(name)

    def __delattr__(self, name):
        """Override the deletion of an attribute.

        If attribute starts with an underscore, delete the attribute from
        the object's __dict__ otherwise delete it from the ordered dict.

        :param name: String name of attribute to delete

        """
        if name in self.__dict__:
            return super(StyleRule, self).__delattr__(name)
        return self.__delitem__(name)

    def __setattr__(self, name, val):
        """Override the setting of an attribute.

        If name is in the pre-defined attributes, call the attribute's
        descriptor's __set__ function. Otherwise, add it to ordered dict as-is.

        :param name: The attribute name
        :param val: The value to set

        """
        if name.startswith("_"):
            return super(StyleRule, self).__setattr__(name, val)
        elif name in self._attributes:
            return self._attributes[name].__set__(self, val)
        return self._add_value(name, val)

    def __setitem__(self, key, value, **kwargs):
        """Override the setting of an attribute in ordered dict.

        If key is in pre-defined attributes, call attribute's descriptor's
        __set__ function. Otherwise add the value to ordered dict as-is.

        :param key: The hash key of the ordered dict
        :param value: The value to map to hash key

        """
        if key in self._attr_options:
            key = key.replace("-", "_")
            try:
                return self._attributes[key].__set__(self, value)
            except KeyError:
                pass
        return self._add_value(key, value, **kwargs)

    def __deepcopy__(self, memo):
        """Override deepcopy.

        Make a deepcopy of all member attributes as well as all substyle rules
        in ordered dictionary.

        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        result.clear()
        for k, v in self.items():
            if isinstance(v, StyleRule):
                v._parent = result
            result._add_value(k, copy.deepcopy(v, memo))
        result._parent = self._parent
        return result

    def __repr__(self, *args, **kwargs):
        """Set the representation to look like xml syntax."""
        return "<{0} name='{1}' />".format(
            self.__class__.__name__, self.name
        )

    def __str__(self):
        """Call to_string if StyleRule is cast to string."""
        return self.to_string()


class StyleSheet(StyleRule,
                 qstylizer.setter.qclass.ClassStyleSetter):
    """The StyleSheet definition.

    Contains descriptors for all class and property options.

    """
    def is_global_scope(self):
        """Determine if style is global scope.

        A StyleSheet is global scope if it has no substyles.
        Resulting string should contain no brackets.
        ::

            background-color: red;
            border: none;

        """
        return self.is_leaf()

    def to_string(self, cascade=True):
        """Return the selector and properties as a single string.

        :param cascade: If True, loop through all substyles to generate a stylesheet.

        """
        if cascade:
            return self._stylesheet()
        style_format = "{selector} {{\n{properties}}}\n"
        prop_format = "    {}: {};\n"
        selector = self.selector
        if self.is_global_scope():
            style_format = "{properties}"
            prop_format = "{}: {};\n"
        else:
            selector = "*"
        properties = ""
        sheet = ""
        for key, value in self.items():
            if not isinstance(value, StyleRule):
                properties += prop_format.format(key, value)
        if properties:
            sheet = style_format.format(**locals())
        return sheet

    @property
    def name(self):
        """Return the name of the StyleSheet."""
        return self._name

    def __repr__(self, *args, **kwargs):
        """Set the representation to look like xml syntax."""
        template = "<{0} />"
        if self.name:
            template = "<{0} name='{1}' />"
        return template.format(
            self.__class__.__name__, self.name
        )


class ClassRule(StyleRule,
                qstylizer.setter.subcontrol.SubControlSetter,
                qstylizer.setter.pseudostate.PseudoStateSetter):
    """The ClassRule definition.

    Example class style name: "QCheckBox".
    Contains descriptors for all subcontrols and pseudostates.

    """


class ObjectRule(ClassRule):
    """The ObjectRule definition.

    Example object style name: "#objectName".
    Inherits from ClassRule. Only difference is "#" is the scope operator.

    """
    @property
    def scope_operator(self):
        return "#"


class ChildClassRule(ClassRule):
    """The ChildClassRule definition.

    Example object style name: " QFrame".
    Inherits from ClassRule.
    ::

        QWidget QFrame {
            property: value
        }

    """
    @property
    def scope_operator(self):
        return " "


class ObjectPropRule(StyleRule):
    """The ObjectPropRule definition.

    Example object property style name: "[echoMode="2"]".

    """
    @property
    def scope_operator(self):
        return ""


class StyleRuleList(StyleRule):
    """The StyleRuleList definition.

    Example style list name: "QCheckBox, QComboBox".

    """

    @staticmethod
    def _sanitize_key(key):
        """Strip the key of newlines only."""
        return str(key).replace("\n", "")

    def _find_or_create_values_in_parent(self, name, val):
        """Find or create value in parent StyleRule

        Will loop through all components in name separated by a comma and set the
        property in each of the substyles in the parent StyleRule.

        :param name: The attribute name
        :param val: The value

        """
        style_names = self.name.split(",")
        for style_name in style_names:
            self._parent.find_or_create_value(style_name).__setattr__(name, val)
        return None

    @property
    def scope_operator(self):
        return ""

    def __setattr__(self, name, val):
        """Override the setting of an attribute.

        :param name: The attribute name
        :param val: The value to set

        """
        if name.startswith("_"):
            return super(StyleRule, self).__setattr__(name, val)
        return self._find_or_create_values_in_parent(name, val)

    def __setitem__(self, key, value, **kwargs):
        """Override the setting of a value in ordered dict.

        :param key: The hash key of the ordered dict
        :param value: The value to map to hash key

        """
        return self._find_or_create_values_in_parent(key, value)

    @property
    def name(self):
        """Return the name with no spaces."""
        return self._name.replace(" ", "")


class SubControlRule(StyleRule, qstylizer.setter.pseudostate.PseudoStateSetter):
    """The SubControlRule definition.

    Example subcontrol name: "::indicator".

    """
    @property
    def scope_operator(self):
        return "::"


class PseudoStateRule(SubControlRule):
    """The PseudoStateRule definition.

    Example pseudostate name: ":hover".

    """
    @property
    def scope_operator(self):
        return ":"




