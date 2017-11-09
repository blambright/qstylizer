# -*- coding: utf-8 -*-

import pytest


@pytest.fixture
def css():
    import qstylizer.style
    return qstylizer.style.Style()


@pytest.fixture
def style():
    import qstylizer.style
    return qstylizer.style.Style
