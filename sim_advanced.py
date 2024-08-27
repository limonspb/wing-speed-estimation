# aircraft.py
import math

class Sim_advanced:
    def __init__(self):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.mass = 1
        self.twr = 4
        self.pitch_speed100 = 73
        self.drag_coefficient = 0.0045
        # self.max_speed = TODO
        self.thrust = self.twr * self.mass * self.g

    def get_acceleration(self, speed, pitch, trottle):
        drag_force = self.drag_coefficient * speed**2
        thrust_coef = trottle ** 2 * (1 - speed / (trottle * self.pitch_speed100)) if trottle > 0 else 0
        thrust_force = thrust_coef * self.thrust
        gravity_force = - self.mass * self.g * math.sin(pitch)
        net_force = thrust_force - drag_force - gravity_force
        a = net_force / self.mass
        return a
