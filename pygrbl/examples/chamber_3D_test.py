"""
Part of pygrbl

Example of script of how to use pygrbl.
All lengths are in millimeters.

Noah Stieler, 2023
"""
import time
import math

import pygrbl
from pygrbl import Point

"""
    Different baud rate is required because GRBL 0.8 is being used.
"""
pygrbl.core.BAUD_RATE = 9600
pygrbl.core.FEED_RATE = 200

port = 'COM3'

chamber_radius = 50
chamber_height = 100
padding = 10
# Using metallic sphere with 5cm diameter.
target_radius = 25
target_height = 50

def main():
    chamber = pygrbl.ChamberCylinder3D(chamber_radius, chamber_height,
                                       padding, target_radius, target_height)
    pygrbl.set_chamber(chamber)

    pygrbl_machine = pygrbl.create_pygrbl_machine(port)
    if pygrbl_machine is None:
        print('Failed to connect.')
        return

    pygrbl_machine.set_origin()

    angle = math.pi*0.25
    p = Point(chamber.true_radius*math.cos(angle)*0.98, chamber.true_radius*math.sin(angle)*0.98, -10)
    pygrbl_machine.set_position(p)
    time.sleep(5)
    pygrbl_machine.set_position(Point(0, 0, 0))


if __name__ == '__main__':
    main()
