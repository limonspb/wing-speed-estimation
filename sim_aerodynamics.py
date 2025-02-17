# aircraft.py
import math
import settings
import numpy as np

class Sim_aerodynamics:
    def __init__(self, in_prop_max_speed_gain=1, in_lift_zero=0.0, in_lift_slope=0.1, in_drag_parasitic=0.02, in_drag_induce=0.15):
        self.g = 9.81  # Acceleration due to gravity (m/s^2)
        self.deg_to_rad = math.pi / 180

        self.propPitchMaxSpeed = 0.0004233 * settings.prop_pitch * settings.motor_kv * settings.max_voltage * in_prop_max_speed_gain
        self.max_voltage = settings.max_voltage
        # self.max_speed = TODO
        self.static_thrust = settings.thrust * self.g
        self._lift_zero = in_lift_zero
        self._lift_slope = in_lift_slope
        self._drag_parasitic = in_drag_parasitic
        self._drag_induced = in_drag_induce
        self._wing_area = settings.mass / settings.wing_load
        self._weight = settings.mass * self._g
        
        self._angle_of_attack = 0
        self._path_angle = 0
        
        
    def _get_angle_of_attack(self):
        return self._angle_of_attack
    angle_of_attack = property(fget=_get_angle_of_attack)
    
    def _get_path_angle(self):
        return self._path_angle
    path_angle = property(fget=_get_path_angle)    
        
        
    def _get_airspeed_pressure(self, speed):
        return settings.air_density * speed**2 / 2;
    
    def _get_lift_force_coef(self, speed, load_z):
        speedThreshold = 2.0
        liftActualC = 0
        if speed > speedThreshold:
            liftActualC = load_z * settings.wing_load * 9.81 / self._get_airspeed_pressure(speed);
        liftActualC = min(liftActualC, 1.5)
        liftActualC = max(liftActualC, -1.5)
        return liftActualC
        
    def _get_angle_of_attack_estimate(self, lift_force_c):
        angleOfAttack = (lift_force_c - self._lift_zero) / self._lift_slope;
        return angleOfAttack;
        
    def _calcPlaneSinPathAngle(self, angleOfAttack, pitch, roll):
        #   the velocity unit vector in body frame reference system
        dir_x = math.cos(angleOfAttack)
        dir_y = -math.sin(angleOfAttack)
        
        #   the velocity unit vector earth frame vertical part - sin path angle
        sinPathAngle = -dir_x * math.sin(pitch) + dir_y * math.cos(pitch) * math.cos(roll)
        return sinPathAngle     #sin path angle, >0 - up, <0 down
    
    def _get_drag_force_c(self, lift_force_c):
        return self._drag_parasitic + self._drag_induced * lift_force_c ** 2

    def _get_motor_thrust(self, throttle, voltage, speed):
        scaled_throttle = throttle #* voltage / self.max_voltage
        thrust_coef = scaled_throttle ** 2 - scaled_throttle * speed / (self.propPitchMaxSpeed)
        thrust_force = thrust_coef * self.static_thrust
        return thrust_force
 
    def get_acceleration(self, speed, load_z, roll, pitch, throttle, voltage):
        lift_force_coef = self._get_lift_force_coef(speed, load_z)
        self._angle_of_attack = self._get_angle_of_attack_estimate(lift_force_coef) * self._deg_to_rad
        drag_force = self._get_drag_force_c(lift_force_coef) * self._get_airspeed_pressure(speed) * self._wing_area
        thrust_force = self._get_motor_thrust(throttle, voltage, speed)
        sin_path_angle = self._calcPlaneSinPathAngle(self._angle_of_attack, pitch, roll)
        self._path_angle = math.asin(sin_path_angle)
        load_x = (thrust_force - drag_force) / self._weight
        accel = self._g * (load_x - sin_path_angle)    #classical speed change equition by using of load value
        return accel
