# coding: utf-8

import copy

import qstylizer.setter


class ClassStyleSet(qstylizer.setter.StyleRuleSet):
    """QClass descriptor."""

    def __get__(self, instance, *args, **kwargs):
        """Get the value from the StyleRule's ordered dict.

        If value doesn't exist, create a new PseudoStateRule instance and add it
        to the StyleRule's ordered dict.

        :param instance: The StyleRule instance

        """
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.ClassRule(
                name=self.name,
                parent=instance,
            )
            instance.set_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        """Set the value in the StyleRule's ordered dict.

        If the value is a ClassRule, simply add it to the ordered dict.
        Otherwise create a new ClassRule instance, set its prop_value
        attribute to the value, and add it to the ordered dict.

        :param instance: The StyleRule instance
        :param value: The value to set in StyleRule instance

        """
        import qstylizer.style
        if isinstance(value, qstylizer.style.ClassRule):
            value = copy.deepcopy(value)
            value._parent = instance
            instance.set_value(self.name, value)
        else:
            new_style = qstylizer.style.ClassRule(
                name=self.name,
                parent=instance,
            )
            new_style._prop_value = value
            instance.set_value(self.name, new_style)


class ClassStyleSetter(qstylizer.setter.StyleRuleSetter):
    """QClass setter.

    Contains descriptors for all known QClasses.

    """
    _descriptor_cls = ClassStyleSet

    QAbstractScrollArea = _descriptor_cls("QAbstractScrollArea")
    QCheckBox = _descriptor_cls("QCheckBox")
    QColumnView = _descriptor_cls("QColumnView")
    QComboBox = _descriptor_cls("QComboBox")
    QDateEdit = _descriptor_cls("QDateEdit")
    QDateTimeEdit = _descriptor_cls("QDateTimeEdit")
    QDialog = _descriptor_cls("QDialog")
    QDialogButtonBox = _descriptor_cls("QDialogButtonBox")
    QDockWidget = _descriptor_cls("QDockWidget")
    QDoubleSpinBox = _descriptor_cls("QDoubleSpinBox")
    QFrame = _descriptor_cls("QFrame")
    QGroupBox = _descriptor_cls("QGroupBox")
    QHeaderView = _descriptor_cls("QHeaderView")
    QLabel = _descriptor_cls("QLabel")
    QLineEdit = _descriptor_cls("QLineEdit")
    QListView = _descriptor_cls("QListView")
    QListWidget = _descriptor_cls("QListWidget")
    QMainWindow = _descriptor_cls("QMainWindow")
    QMenu = _descriptor_cls("QMenu")
    QMenuBar = _descriptor_cls("QMenuBar")
    QMessageBox = _descriptor_cls("QMessageBox")
    QProgressBar = _descriptor_cls("QProgressBar")
    QPushButton = _descriptor_cls("QPushButton")
    QRadioButton = _descriptor_cls("QRadioButton")
    QScrollBar = _descriptor_cls("QScrollBar")
    QSizeGrip = _descriptor_cls("QSizeGrip")
    QSlider = _descriptor_cls("QSlider")
    QSpinBox = _descriptor_cls("QSpinBox")
    QSplitter = _descriptor_cls("QSplitter")
    QStatusBar = _descriptor_cls("QStatusBar")
    QTabBar = _descriptor_cls("QTabBar")
    QTabWidget = _descriptor_cls("QTabWidget")
    QTableView = _descriptor_cls("QTableView")
    QTableWidget = _descriptor_cls("QTableWidget")
    QTextEdit = _descriptor_cls("QTextEdit")
    QTimeEdit = _descriptor_cls("QTimeEdit")
    QToolBar = _descriptor_cls("QToolBar")
    QToolButton = _descriptor_cls("QToolButton")
    QToolBox = _descriptor_cls("QToolBox")
    QToolTip = _descriptor_cls("QToolTip")
    QTreeView = _descriptor_cls("QTreeView")
    QTreeWidget = _descriptor_cls("QTreeWidget")
    QWidget = _descriptor_cls("QWidget")


