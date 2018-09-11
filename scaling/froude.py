import pint

# Initialise unit definitions
UREG = pint.UnitRegistry()

# Define Froude scaling relationships
LENGTH_EXPONENT = 1
TIME_EXPONENT = 1 / 2
MASS_EXPONENT = 3


def _convert(x, length_scale_factor, input_unit, target_unit):

    # Calculate unit conversion factor
    input_unit = UREG(input_unit)
    target_unit = UREG(target_unit)
    unit_conversion_factor = input_unit.to(target_unit).magnitude

    # Calculate Froude scaling factor
    froude_scale_factor = length_scale_factor**(
        input_unit.dimensionality['[length]'] * LENGTH_EXPONENT +
        input_unit.dimensionality['[time]'] * TIME_EXPONENT +
        input_unit.dimensionality['[mass]'] * MASS_EXPONENT)

    # Scale values
    x_scaled = x * froude_scale_factor

    # Convert to output units
    x_scaled *= unit_conversion_factor

    return x_scaled


def proto_to_model(x_proto,
                   length_scale,
                   input_unit,
                   target_unit,
                   index_input_unit=None,
                   index_target_unit=None):
    """Convert prototype value(s) to model value(s) in specified units.

    Args:
        x_proto:            prototype values (array_like, or pandas dataframe)
        length_scale:       ratio between proto and model dimensions (float)
        input_unit:         unit of input (string)
        target_unit:        unit of output (string)
        index_input_unit:   unit of input index (dataframe only)
        index_target_unit:  unit of output index (dataframe only)

    Returns:
        input values in model scale
    """

    length_scale_factor = 1 / length_scale

    # Convert values
    x_model = _convert(x_proto, length_scale_factor, input_unit, target_unit)

    # Convert index (dataframe or series only)
    if (index_input_unit is not None) and (index_target_unit is not None):
        if type(x_model).__name__ in ['DataFrame', 'Series']:
            x_model.index = _convert(x_model.index, length_scale_factor,
                                     index_input_unit, index_target_unit)
        else:
            raise ValueError("'index_input_unit' and 'index_target_unit' "
                             "can only be used when input is dataframe")

    return x_model


def model_to_proto(x_model,
                   length_scale,
                   input_unit,
                   target_unit,
                   index_input_unit=None,
                   index_target_unit=None):
    """Convert model value(s) to prototype value(s) in specified units.

    Args:
        x_model:            model values (array_like, or pandas dataframe)
        length_scale:       ratio between proto and model dimensions (float)
        input_unit:         unit of input (string)
        target_unit:        unit of output (string)
        index_input_unit:   unit of input index (dataframe only)
        index_target_unit:  unit of output index (dataframe only)

    Returns:
        input values in prototype scale
    """

    length_scale_factor = length_scale

    # Convert values
    x_proto = _convert(x_model, length_scale_factor, input_unit, target_unit)

    # Convert index (dataframe or series only)
    if (index_input_unit is not None) and (index_target_unit is not None):
        if type(x_proto).__name__ in ['DataFrame', 'Series']:
            x_proto.index = _convert(x_proto.index, length_scale_factor,
                                     index_input_unit, index_target_unit)
        else:
            raise ValueError("'index_input_unit' and 'index_target_unit' "
                             "can only be used when input is dataframe")

    return x_proto


def dimensions(unit):
    """Get unit dimensions.

    Args:
        unit:  unit name or symbol (string)

    Returns:
        string containing unit dimensions
    """

    # Get dimensions of unit
    dims = UREG(unit).dimensionality

    dim_data = {'L': '[length]', 'M': '[mass]', 'T': '[time]'}

    s = ''
    for symbol, key in dim_data.items():
        exponent = dims[key]
        if exponent != 0:
            s += '{}^{:g} '.format(symbol, exponent)

    return s.strip()


def scaling_exponent(unit):
    """Convert prototype value(s) to model value(s) in specified units.

    Args:
        unit:  unit of quantity to be scaled (string)

    Returns:
        scaling factor
    """
    # Calculate Froude scaling factor
    scaling_exponent = (UREG(unit).dimensionality['[length]'] * LENGTH_EXPONENT
                        + UREG(unit).dimensionality['[time]'] * TIME_EXPONENT +
                        UREG(unit).dimensionality['[mass]'] * MASS_EXPONENT)

    return scaling_exponent
