import pytest

from pygeoguz.simplegeo import *


def test_ground():
    assert ground(15.45, 1) == 15.4
    assert ground(15.55, 1) == 15.6
    assert ground(15.100, 2) == 15.1
    assert ground(15.445, 4) == 15.445
    assert ground(15.5) == 16

