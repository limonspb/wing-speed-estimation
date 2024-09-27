# aircraft.py
import math
from settings import *

class Sim_basic:
    def __init__(self, in_pitch_offset=0, in_gravity=0.5, in_delay=1):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.twr = 1 / in_gravity**2
        self.mass = (2/math.log(3))**2 * self.twr * self.g * in_delay ** 2
        self.drag_coefficient = 1
        self.max_speed = math.sqrt(self.mass * (self.twr * self.g + self.g) / self.drag_coefficient)
        self.max_voltage = max_voltage
        self.pitch_offset = in_pitch_offset

    def get_acceleration(self, speed, pitch, trottle, voltage):
        scaled_throttle = trottle #* voltage / self.max_voltage
        a = scaled_throttle * scaled_throttle * self.twr * self.g - self.drag_coefficient * speed * speed / self.mass + self.g * math.sin(pitch + self.pitch_offset / 180 * math.pi)
        return a
