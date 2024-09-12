# aircraft.py
import math
from settings import *

class Sim_advanced:
    def __init__(self, in_twr=4, in_prop_pitch=4.7, in_drag_k=0.0045):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.mass = mass
        self.twr = in_twr
        self.propPitchMaxSpeed = 0.0004233 * in_prop_pitch * motor_kv * max_voltage
        self.drag_coefficient = in_drag_k
        self.max_voltage = max_voltage
        # self.max_speed = TODO
        self.thrust = self.twr * self.mass * self.g

    def get_acceleration(self, speed, pitch, trottle, voltage):
        scaled_throttle = trottle * voltage / self.max_voltage
        drag_force = self.drag_coefficient * speed**2
        thrust_coef = scaled_throttle ** 2 - scaled_throttle * speed / self.propPitchMaxSpeed
        thrust_force = thrust_coef * self.thrust
        gravity_force = - self.mass * self.g * math.sin(pitch)
        net_force = thrust_force - drag_force - gravity_force
        a = net_force / self.mass
        return a
