import pytest
from scaling import froude

def test_unit_to_same_unit():
    assert froude.model_to_proto(1, 1, 'm', 'm') == 1

def test_froude_length():
    assert froude.model_to_proto(1, 10, 'm', 'm') == 10

def test_froude_force():
    assert froude.model_to_proto(1, 10, 'N', 'N') == 1000

def test_unit_dimensions():
    assert froude.dimensions('m') == 'L^1'
    assert froude.dimensions('kg') == 'M^1'
    assert froude.dimensions('s') == 'T^1'
    assert froude.dimensions('N') == 'L^1 M^1 T^-2'
