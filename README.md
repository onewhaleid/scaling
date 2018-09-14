# scaling

Convert quantities between model and prototype scale using Froude similarity.

## Installation

```
pip install git+http://git.wrl.unsw.edu.au:3000/danh/scaling.git
```

## Usage

```sh
>>> from scaling import Froude
>>> froude = FroudeConverter()

>>> # Convert model value of 200 mm to prototype value (m) with scale of 10
>>> froude.model_to_proto(200, length_scale=10, input_unit='mm', target_unit='m')
2.0

>>> # Get Froude scaling exponent for quantities of time
>>> froude.scaling_exponent('s')
0.5

>>> # Get length, mass and time dimensions for quantities of force
>>> froude.dimensions('N')
'L^1 M^1 T^-2'
```

`scaling` uses `pint` for unit and dimension conversions. `pint` is able to interpret a wide range of different input units.

```sh
>>> # Convert water head model value (mm) to prototype pressure value (kPa)
>>> froude.model_to_proto(10, length_scale=100, 'mm.H20', 'kPa')
9.80665

>>> # Make sure gravity remains constant in Froude scaling
>>> froude.proto_to_model(1, 10, 'gravity', 'meter/second/second')
9.80665
```
