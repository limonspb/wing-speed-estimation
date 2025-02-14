# aircraft.py
import math
import settings
import numpy as np

class Sim_aerodynamics:
    def __init__(self, in_thrust=4, in_prop_pitch=4.7, in_lift_zero=0.0, in_lift_slope=0.1, in_drag_parasitic=0.02, in_drag_induce=0.2):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.deg_to_rad = math.pi / 180

        self.twr = in_thrust / settings.mass
        self.propPitchMaxSpeed = 0.0004233 * in_prop_pitch * settings.motor_kv * settings.max_voltage
        self.max_voltage = settings.max_voltage
        # self.max_speed = TODO
        self.thrust = self.twr * settings.mass * self.g

        self.lift_zero = in_lift_zero
        self.lift_slope = in_lift_slope
        self.drag_parasitic = in_drag_parasitic
        self.drag_induced = in_drag_induce
        self.wing_area = settings.mass / settings.wing_load
        self.weight = settings.mass * self.g
        
    def get_airspeed_pressure(self, speed):
        return settings.air_density * speed**2 / 2;
    
    def get_lift_force_coef(self, speed, load_z):
        speedThreshold = 2.0
        liftActualC = 0
        if speed > speedThreshold:
            liftActualC = load_z * settings.wing_load * 9.81 / self.get_airspeed_pressure(speed);
        liftActualC = min(liftActualC, 1.5)
        liftActualC = max(liftActualC, -1.5)
        return liftActualC
        
    def get_angle_of_attack_estimate(self, lift_force_c):
        angleOfAttack = (lift_force_c - self.lift_zero) / self.lift_slope;
        return angleOfAttack;
        
    def calcPlaneSinPathAngle(self, angleOfAttack, pitch, roll):
        #   the velocity unit vector in body frame reference system
        dir_x = math.cos(angleOfAttack)
        dir_y = -math.sin(angleOfAttack)
        
        #   the velocity unit vector earth frame vertical part - sin path angle
        sinPathAngle = -dir_x * math.sin(pitch) + dir_y * math.cos(pitch) * math.cos(roll)
        return sinPathAngle     #sin path angle, >0 - up, <0 down
    
    def get_drag_force_c(self, lift_force_c):
            return self.drag_parasitic + self.drag_induced * lift_force_c ** 2

    def get_motor_thrust(self, throttle, voltage, speed):
        scaled_throttle = throttle #* voltage / self.max_voltage
        thrust_coef = scaled_throttle ** 2 - scaled_throttle * speed / (self.propPitchMaxSpeed)
        thrust_force = thrust_coef * self.thrust
        return thrust_force
 
    def get_acceleration(self, speed, load_z, roll, pitch, throttle, voltage):
        lift_force_coef = self.get_lift_force_coef(speed, load_z)
        angle_of_attack = self.get_angle_of_attack_estimate(lift_force_coef) * self.deg_to_rad
        drag_force = self.get_drag_force_c(lift_force_coef) * self.get_airspeed_pressure(speed) * self.wing_area
        thrust_force = self.get_motor_thrust(throttle, voltage, speed)
        sin_path_angle = self.calcPlaneSinPathAngle(angle_of_attack, pitch, roll)
        load_x = (thrust_force - drag_force) / self.weight
        accel = self.g * (load_x - sin_path_angle)    #classical speed change equition by using of load value
        return accel
