import pint

# Initialise unit definitions
UREG = pint.UnitRegistry()

# Define Froude scaling relationships
LENGTH_EXPONENT = 1
TIME_EXPONENT = 1 / 2
MASS_EXPONENT = 3


def _convert(x, length_scale_factor, from_unit, to_unit):

    # Calculate unit conversion factor
    from_unit = UREG(from_unit)
    to_unit = UREG(to_unit)
    unit_conversion_factor = from_unit.to(to_unit).magnitude

    # Calculate Froude scaling factor
    froude_scale_factor = length_scale_factor**(
        from_unit.dimensionality['[length]'] * LENGTH_EXPONENT +
        from_unit.dimensionality['[time]'] * TIME_EXPONENT +
        from_unit.dimensionality['[mass]'] * MASS_EXPONENT)

    # Scale values
    x_scaled = x * froude_scale_factor

    # Convert to output units
    x_scaled *= unit_conversion_factor

    # Scale time (dataframe or series only)
    try:
        x_scaled.index *= length_scale_factor**TIME_EXPONENT
    except (AttributeError, TypeError):
        pass

    return x_scaled


def proto_to_model(x_proto, length_scale, from_unit, to_unit):
    """Convert prototype value(s) to model value(s) in specified units.

    Args:
        x_proto:          prototype values (array_like, or pandas dataframe)
        length_scale:     ratio between prototype and model dimensions (float)
        from_unit (str):  unit of input value(s)
        to_unit (str):    unit of output value(s)

    Returns:
        input values in model scale
    """

    length_scale_factor = 1 / length_scale

    return _convert(x_proto, length_scale_factor, from_unit, to_unit)


def model_to_proto(x_model, length_scale, from_unit, to_unit):
    """Convert model value(s) to prototype value(s) in specified units.

    Args:
        x_model:          model values (array_like, or pandas dataframe)
        length_scale:     ratio between prototype and model dimensions (float)
        from_unit (str):  unit of input value(s)
        to_unit (str):    unit of output value(s)

    Returns:
        input values in prototype scale
    """

    length_scale_factor = length_scale

    return _convert(x_model, length_scale_factor, from_unit, to_unit)


def dimensions(unit):
    """Get unit dimensions.

    Args:
        unit (str):  unit name or symbol

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
