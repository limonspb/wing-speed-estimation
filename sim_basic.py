# aircraft.py
import math

class Sim_basic:
    def __init__(self, gravity=0.5, delay=1):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.twr = 1 / gravity**2
        self.mass = (2/math.log(3))**2 * self.twr * self.g * delay ** 2
        self.drag_coefficient = 1
        self.max_speed = math.sqrt(self.mass * (self.twr * self.g + self.g) / self.drag_coefficient)
        self.max_voltage = 4.2 * 6

    def get_acceleration(self, speed, pitch, trottle, voltage):
        scaled_throttle = trottle * voltage / self.max_voltage
        a = scaled_throttle * scaled_throttle * self.twr * self.g - self.drag_coefficient * speed * speed / self.mass + self.g * math.sin(pitch)
        return a
