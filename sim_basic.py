# aircraft.py
import math

class Sim_basic:
    def __init__(self, twr=4, drag_coefficient=0.0045):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.mass = 1
        self.twr = twr
        self.drag_coefficient = drag_coefficient
        self.max_speed = math.sqrt(self.mass * (self.twr * self.g + self.g) / self.drag_coefficient)
        self.max_voltage = 4.2 * 6

    def get_acceleration(self, speed, pitch, trottle, voltage):
        scaled_throttle = trottle * voltage / self.max_voltage
        a = scaled_throttle * scaled_throttle * self.twr * self.g - self.drag_coefficient * speed * speed / self.mass + self.g * math.sin(pitch)
        return a
