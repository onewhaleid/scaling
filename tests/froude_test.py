import pandas as pd
import pytest
from scaling import froude

def test_unit_to_same_unit():
    assert froude.model_to_proto(1, 1, 'm', 'm') == 1
    assert froude.proto_to_model(1, 1, 'm', 'm') == 1

def test_unit_to_different_unit():
    assert froude.model_to_proto(1, 1, 'kN', 'N') == 1000
    assert froude.proto_to_model(1000, 1, 'N', 'kN') == 1

def test_froude_length():
    assert froude.model_to_proto(1, 10, 'm', 'm') == 10

def test_froude_time():
    assert froude.model_to_proto(1, 25, 's', 's') == 5

def test_froude_force():
    assert froude.model_to_proto(1, 10, 'N', 'N') == 1000

def test_froude_time_index_dataframe():
    df_model = pd.DataFrame(index=[2], data=[20])
    df_proto = froude.model_to_proto(df_model, 16, 'mm', 'm', 's', 's')
    assert df_proto.index.values[0] == 8

def test_froude_mass_index_dataframe():
    df_proto = pd.DataFrame(index=[4], data=[16])
    df_model = froude.proto_to_model(df_proto, 2, 'kN', 'N', 'm', 'm')
    assert df_model.index.values[0] == 2

def test_unit_dimensions():
    assert froude.dimensions('m') == 'L^1'
    assert froude.dimensions('kg') == 'M^1'
    assert froude.dimensions('s') == 'T^1'
    assert froude.dimensions('N') == 'L^1 M^1 T^-2'

def test_scaling_exponent():
    assert froude.scaling_exponent('m') == 1
    assert froude.scaling_exponent('kg') == 3
    assert froude.scaling_exponent('s') == 0.5
