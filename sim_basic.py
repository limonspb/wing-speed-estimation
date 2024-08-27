# aircraft.py
import math

class Sim_basic:
    def __init__(self):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.mass = 1
        self.twr = 4
        self.drag_coefficient = 0.0045
        self.max_speed = math.sqrt(self.mass * (self.twr * self.g + self.g) / self.drag_coefficient)

    def get_acceleration(self, speed, pitch, trottle):
        a = trottle * trottle * self.twr * self.g - self.drag_coefficient * speed * speed / self.mass + self.g * math.sin(pitch)
        return a
