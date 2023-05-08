import pytest

from common.utils import date_fibonacci


@pytest.fixture()
def day_fibonacci():
    return date_fibonacci()
