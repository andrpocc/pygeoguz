import pytest

from pygeoguz.simplegeo import *


def test_ground():
    assert ground(15.45, 1) == 15.4
    assert ground(15.55, 1) == 15.6
    assert ground(15.100, 2) == 15.1
    assert ground(15.445, 4) == 15.445
    assert ground(15.95, 1) == 16.0
    assert ground(15.85, 1) == 15.8
    assert ground(15.5) == 16
    assert ground(39.5) == 40
    assert ground(38.5) == 38
    assert ground(38.5) == 38
    assert ground(38.44, 1) == 38.4
    assert ground(38.46, 1) == 38.5
    assert ground(38.572, 2) == 38.57
    assert ground(38.575, 2) == 38.58
    assert ground(38.579, 2) == 38.58
    assert ground(38.595, 2) == 38.60
