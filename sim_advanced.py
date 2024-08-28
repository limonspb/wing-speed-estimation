# aircraft.py
import math

class Sim_advanced:
    def __init__(self, twr=4, pitch_speed100=73, drag_coefficient=0.0045):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.mass = 1.1
        self.twr = twr
        self.pitch_speed100 = pitch_speed100
        self.drag_coefficient = drag_coefficient
        self.max_voltage = 4.2 * 6
        # self.max_speed = TODO
        self.thrust = self.twr * self.mass * self.g

    def get_acceleration(self, speed, pitch, trottle, voltage):
        scaled_throttle = trottle * voltage / self.max_voltage
        drag_force = self.drag_coefficient * speed**2
        thrust_coef = scaled_throttle ** 2 * (1 - speed / (scaled_throttle * self.pitch_speed100)) if scaled_throttle > 0 else 0
        thrust_force = thrust_coef * self.thrust
        gravity_force = - self.mass * self.g * math.sin(pitch)
        net_force = thrust_force - drag_force - gravity_force
        a = net_force / self.mass
        return a
