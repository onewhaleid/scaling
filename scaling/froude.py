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

    # Scale time (dataframe or series only)
    try:
        x_scaled.index *= length_scale_factor**TIME_EXPONENT
    except (AttributeError, TypeError):
        pass

    return x_scaled


def proto_to_model(x_proto, length_scale, input_unit, target_unit):
    """Convert prototype value(s) to model value(s) in specified units.

    Args:
        x_proto:       prototype values (array_like, or pandas dataframe)
        length_scale:  ratio between prototype and model dimensions (float)
        input_unit:    unit of input (string)
        target_unit:   unit of output (string)

    Returns:
        input values in model scale
    """

    length_scale_factor = 1 / length_scale

    return _convert(x_proto, length_scale_factor, input_unit, target_unit)


def model_to_proto(x_model, length_scale, input_unit, target_unit):
    """Convert model value(s) to prototype value(s) in specified units.

    Args:
        x_model:       model values (array_like, or pandas dataframe)
        length_scale:  ratio between prototype and model dimensions (float)
        input_unit:    unit of input (string)
        target_unit:   unit of output (string)

    Returns:
        input values in prototype scale
    """

    length_scale_factor = length_scale

    return _convert(x_model, length_scale_factor, input_unit, target_unit)


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
