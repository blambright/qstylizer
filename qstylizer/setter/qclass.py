# -*- coding: utf-8 -*-

import copy

import qstylizer.setter


class ClassStyleSet(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        import qstylizer.style
        assert isinstance(instance, qstylizer.style.StyleRule)
        if instance.find_value(self.name) is None:
            new_style = qstylizer.style.ClassStyleRule(
                name=self.name,
                parent=instance,
            )
            instance._add_value(self.name, new_style)
        return instance.find_value(self.name)

    def __set__(self, instance, value):
        import qstylizer.style
        if not isinstance(value, qstylizer.style.ClassStyleRule):
            raise ValueError("Can only assign a ClassStyleRule style.")
        value = copy.deepcopy(value)
        value._is_root = False
        value._parent = instance
        instance._add_value(self.name, value)


class ClassStyleSetter(qstylizer.setter.Setter):

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

