import pandas as pd
import pytest
from scaling import ReynoldsConverter

reynolds = ReynoldsConverter()


def test_unit_to_same_unit():
    assert reynolds.model_to_proto(1, 1, 'm', 'm') == 1
    assert reynolds.proto_to_model(1, 1, 'm', 'm') == 1


def test_unit_to_different_unit():
    assert reynolds.model_to_proto(1, 1, 'kN', 'N') == 1000
    assert reynolds.proto_to_model(1000, 1, 'N', 'kN') == 1


def test_reynolds_length():
    assert reynolds.model_to_proto(1, 10, 'm', 'm') == 10
    assert reynolds.proto_to_model(10, 10, 'm', 'm') == 1


def test_reynolds_time():
    assert reynolds.model_to_proto(1, 5, 's', 's') == 25
    assert reynolds.proto_to_model(25, 5, 's', 's') == pytest.approx(1, 0.01)


def test_reynolds_force():
    assert reynolds.model_to_proto(1, 10, 'N', 'N') == 1
    assert reynolds.proto_to_model(1000, 10, 'N', 'N') == 1000


def test_reynolds_overtopping():
    assert reynolds.model_to_proto(10, 4, 'L/m/s', 'L/m/s') == 10
    assert reynolds.proto_to_model(100, 50, 'L/m/s', 'L/m/s') == 100


def test_reynolds_time_index_dataframe():
    df_model = pd.DataFrame(index=[2], data=[2])
    df_proto = reynolds.model_to_proto(df_model, 16, 'mm', 'm', 's', 's')
    assert df_proto.index.values[0] == 512


def test_reynolds_length_index_dataframe():
    df_proto = pd.DataFrame(index=[4], data=[16])
    df_model = reynolds.proto_to_model(df_proto, 2, 'kN', 'N', 'm', 'm')
    assert df_model.index.values[0] == 2


def test_unit_dimensions():
    assert reynolds.dimensions('m') == 'L^1'
    assert reynolds.dimensions('kg') == 'M^1'
    assert reynolds.dimensions('s') == 'T^1'
    assert reynolds.dimensions('N') == 'L^1 M^1 T^-2'
    assert reynolds.dimensions('Pa') == 'L^-1 M^1 T^-2'
    assert reynolds.dimensions('L/m/s') == 'L^2 T^-1'
    assert reynolds.dimensions('mm^2.s') == 'L^2 T^1'


def test_scaling_exponent():
    assert reynolds.scaling_exponent('m') == 1
    assert reynolds.scaling_exponent('kg') == 3
    assert reynolds.scaling_exponent('s') == 2
    assert reynolds.scaling_exponent('N') == 0
    assert reynolds.scaling_exponent('Pa') == -2
    assert reynolds.scaling_exponent('L/m/s') == 0
    assert reynolds.scaling_exponent('mm^2.s') == 4
