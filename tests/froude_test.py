import pytest
from scaling import froude

def test_unit_to_same_unit():
    assert froude.model_to_proto(1, 1, 'm', 'm') == 1

def test_froude_length():
    assert froude.model_to_proto(1, 10, 'm', 'm') == 10

def test_froude_force():
    assert froude.model_to_proto(1, 10, 'N', 'N') == 1000
