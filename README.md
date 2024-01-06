# pygrbl

`pygrbl` provides a simple interface for controlling grbl-based
cartesian robots (https://github.com/grbl/grbl) via USB. This package was developed 
as part of Algae (https://github.com/kelpdotkelp/Algae).

Before positioning is enabled, you must pass a valid `PyGRBLChamber`
object to `set_chamber`, and call `PyGRBLMachine.set_origin()`. Note:
if the origin or the chamber geometry is not set correctly you risk 
the target colliding with the chamber as all of `pygrbl` error checking depends
upon correctly setting those parameters.

See `/pygrbl/examples/simple_test.py` for more detail on how to configure `pygrbl`.

All distances are in millimeters.

## Documentation

## Classes

### `PyGRBLMachine`

Main class for controlling a cartesian robot. Should not be instantiated directly,
use `create_pygrbl_machine` instead.

`PyGRBLMachine.__init__(address: str)`

`PyGRBLMachine.set_origin()`

Sets the origin of the machine to its current physical position.

`PyGRBLMachine.set_position(self, pos_new: Point)`

pos_new -> Next position to move to.

Attempts to move to the specified position. Queries the controller while
moving to ensure target remains within chamber bounds.

### `PyGRBLChamber`

Base class for all chamber geometries.

`is_point_valid(point: Point)`

Implemented by subclasses, returns a boolean indicating whether
`point` is valid to move to based on the subclass chamber geometry and
target geometry.

### `ChamberCircle2D(PyGRBLChamber)`

Specifies a chamber geometry of a circle in the XY plane with a
circular target inside it.

`ChamberCircle2D.__init__(self, radius: float, padding: float, target_radius: float)`

radius -> The measured radius of the chamber.

padding -> Extra distance away from edge of chamber that target can not enter.

target_radius -> Cross-sectional radius of the target. Non-circular targets can
be used by first bounding them with a circle to get their radius.


`@property ChamberCircle2D.true_radius`

Circle which points can actually be in, calculated as:

self.radius - self.padding - self.target_radius

`ChamberCircle2D.is_point_valid(point: Point)`

See superclass definition.

`@staticmethod ChamberCircle2D.gen_rand_uniform(num_points: int, radius: float, order='none')`

num_points -> Number of points to generate.

radius -> radius of circle to generate them in.

order -> 'none' or 'nearest_neighbour' how to order the points once generated.

Returns a list of uniformly distributed points with the specified radius.

### `ChamberCylinder3D(PyGRBLChamber)`

Specifies a chamber geometry of a cylinder in the XYZ plane, with
a cylindrical target. The origin is taken at the center of the cylinder,
on the top face.

`ChamberCylinder3D.__init__(self, radius: float, height: float, padding: float,
target_radius: float, target_height: float)`

radius -> Radius of the chamber.

height -> Height of the chamber.

padding -> Extra distance away from the chamber edges that the target can not enter.

target_radius -> Radius of the target.

target_height -> Height of the target.

For a spherical target, target_radius would be the sphere's radius, target_height
would be the sphere's diameter.

`@property ChamberCylinder3D.true_radius`

Circle which XY points can actually be in, calculated as:

self.radius - self.padding - self.target_radius

`@property ChamberCylinder3D.true_height`

Boundary in the Z direction for points, calculated as:

self.height - self.padding - self.target_height/2

`ChamberCircle2D.is_point_valid(point: Point)`

See superclass definition.

### `Point`

Represents points in 3D cartesian coordinates.

Instance attributes:
Point.x, Point.y, Point.z, Point.mag

`Point.dist(other: Point)`

Returns the distance between this instance and `other`.

## Functions

`create_pygrbl_machine`

address -> Serial port that the GRBL controller is connected to, ex. COM4.

Returns an instance of `PyGRBLMachine` if the serial connection was successful,
otherwise, it returns `None`.

`set_chamber(chamber: PyGRBLChamber)`

Sets the physical dimensions of the chamber and target being moved. 
Calling `set_chamber` is required before positioning is enabled.

`load_csv(path: str, dimension: int)`

path -> Absolute path of a .csv file
dimension -> How many components each point has (2 or 3).

Parses a .csv file of floats and returns a list of `Point` objects.




