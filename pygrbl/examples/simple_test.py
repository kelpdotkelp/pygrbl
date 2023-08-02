"""
Part of pygrbl

Example of script of how to use pygrbl.

Noah Stieler, 2023
"""
import pygrbl
from pygrbl import Point

port = 'COM4'
target_radius = 20


def main():
    # Set up chamber geometry
    chamber = pygrbl.ChamberCircle2D(140, target_radius, 20)
    pygrbl.set_chamber(chamber)

    pygrbl_machine = pygrbl.create_pygrbl_machine(port)
    if pygrbl_machine is None:
        print('Failed to connect.')
        return

    # Set machine origin
    pygrbl_machine.set_origin()

    # Generate list of positions
    pos_list = pygrbl.ChamberCircle2D.gen_rand_uniform(5, target_radius, order='nearest_neighbour')
    # pos_list = [Point(10, 10), Point(78, 79)]

    # Travel to every position in pos_list
    for pos in pos_list:
        pygrbl_machine.set_position(pos)

    # Return to origin
    pygrbl_machine.set_position(Point(0, 0))


if __name__ == '__main__':
    main()
