"""
Part of pygrbl

Implements the main class responsible for sending Gcode.

Noah Stieler, 2023
"""

import serial
import time

from .geometry import *
from .exception import *

FEED_RATE: float = 400  # mm/min
BAUD_RATE: int = 115200
TIMEOUT: float = 1  # seconds
MOVE_WAIT_TIME: float = 0  # seconds, how long to sleep after moving to a new position.

_chamber: PyGRBLChamber = None


class PyGRBLMachine:
    def __init__(self, address):
        self.ser: serial.Serial = None
        self.origin_set: bool = False
        self.prev_pos: Point = None

        self._connect(address)

    def __del__(self):
        if self.ser is not None:
            self.ser.close()

    def set_origin(self) -> None:
        """Sets the origin at the machine's current position"""
        try:
            self._send_command('G90')  # Absolute positioning
            self._send_command('G92 X0 Y0 Z0')  # Set origin point
            self._send_command('G21')  # All units in mm
        except CommandException:
            raise
        self.origin_set = True

    def set_position(self, pos_new: Point) -> None:
        """Attempts to move to a new position. Delays are put in place to ensure
        VNA does not fire while there is still movement."""
        if not self.origin_set:
            raise OriginNotSetException
        if _chamber is None:
            raise ChamberNotDefinedException
        if not _chamber.is_point_valid(pos_new):
            raise PointOutOfBoundsException

        try:
            time.sleep(0.5)
            self._send_command(f'G1 F{FEED_RATE} X{pos_new.x} Y{pos_new.y} Z{pos_new.z}')

            # Wait until movement has been completed.
            idle_state = False
            while not idle_state:
                out = self._send_command('?')  # Query status
                for string in out:
                    if string[0] == '<':
                        end = string.find('|')

                        # Check while moving that machine is in bounds
                        if string[1:end] == 'Run':
                            query_x = string[string.find(':') + 1: string.find(',')]
                            query_y = string[string.find(',') + 1: string.find(',', string.find(',') + 1)]
                            moving_pos = Point(float(query_x), float(query_y))
                            if not _chamber.is_point_valid(moving_pos):
                                self._send_command('!')  # Feed stop
                                raise PointOutOfBoundsException

                        if string[1:end] == 'Idle':
                            idle_state = True
            time.sleep(MOVE_WAIT_TIME)
        except CommandException:
            raise

    def _connect(self, address: str) -> None:
        if self.ser is not None:
            self.ser.close()

        try:
            self.ser = serial.Serial(address, baudrate=BAUD_RATE, timeout=TIMEOUT)

            self.ser.write('\r\n\r\n'.encode('utf-8'))
            time.sleep(2)
            self.ser.flushInput()
        except serial.serialutil.SerialException as e:
            self.ser = None

    def _send_command(self, cmd: str) -> list:
        self.ser.write((cmd + '\n').encode('utf-8'))
        out = self.ser.readlines()

        for i in range(len(out)):
            out[i] = out[i].decode('utf-8')
            out[i] = out[i][:-2]  # Remove \r\n

            # Status command begins with a '<'
            if not (out[i] == 'ok' or out[i][0] == '<'):
                raise CommandException(cmd)

        return out


def create_pygrbl_machine(address: str) -> PyGRBLMachine:
    new_machine = PyGRBLMachine(address)
    if new_machine.ser is not None:
        return new_machine
    else:
        return None


def set_chamber(chamber: PyGRBLChamber) -> None:
    global _chamber
    _chamber = chamber
