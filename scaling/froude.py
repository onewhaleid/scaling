import pint


def _convert(x, length_scale_factor, from_unit, to_unit):

    # Initialise unit definitions
    ureg = pint.UnitRegistry()

    # Calculate unit conversion factor
    from_unit = ureg[from_unit]
    to_unit = ureg[to_unit]
    unit_conversion_factor = (1 * from_unit).to(to_unit).magnitude

    # Define Froude scaling relationships
    froude_l_exponent = 1
    froude_t_exponent = 1 / 2
    froude_m_exponent = 3

    # Calculate Froude scaling factor
    froude_scale_factor = length_scale_factor**(
        from_unit.dimensionality['[length]'] * froude_l_exponent +
        from_unit.dimensionality['[time]'] * froude_t_exponent +
        from_unit.dimensionality['[mass]'] * froude_m_exponent)

    # Scale time (dataframe only)
    try:
        x.index *= length_scale_factor**froude_t_exponent
    except AttributeError:
        pass

    # Scale values
    x *= froude_scale_factor

    # Convert to output units
    x *= unit_conversion_factor

    return x


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
