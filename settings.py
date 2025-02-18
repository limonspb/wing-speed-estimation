import math
import os

# change this between True/False if you need to run automatic parameters finding
calculate = True

# user defined parameters
max_voltage = 25.2 # volts
#max_voltage = 12.6 # volts
mass = 1.72 # kilograms
motor_kv = 1960
#motor_kv = 4533

# ranges of parameters for the automatic algorithm to find best values
range_pitch_offset = [-5, 5] # degrees

range_delay = (0.1, 10) # seconds
range_gravity = (0.1, 10) # percents / 100

range_thrust = (0.5, 10.0) # kilograms
#range_thrust = (0.1, 1.5) # kilograms
range_prop_pitch = (1.1, 7.0) # inches
range_drag_k = (0.0001, 0.05)

# parameters to plot with, when automatic parameters finding is False (OFF)
prop_pitch = 4.1 # inches
drag_k = 0.0046
thrust = 2.5 # kilograms
pitch_offset_basic = 15 # degrees
pitch_offset_advanced = 0 # degrees

tpa_delay = 0.5
tpa_gravity = 0.5

dt_target = 0.01
time_start = 200
time_stop = 221

thrust_aerodynamics = 2.5 # kilograms
prop_pitch_aerodynamics = 4.1 # inches
# aerodynamics parameters
wing_load = 5.57     #kg/m^2
air_density = 1.225 #
lift_zero = 0.01
lift_slope = 0.1
drag_parasitic = 0.03
drag_induced = 0.2


range_lift_zero = (-0.1, 0.1)
range_lift_slope = (0.05, 0.2)
range_drag_parasitic = (0.01, 0.08)
range_drag_induced = (0.1, 0.4)

def print_cli_settings():
    settings_text = (
        f"\n"
        f"XXXX print_cli_settings: PID: {os.getpid()}, Called print_cli_settings()\n"
        f"#========================================\n"
        f"set tpa_speed_type = BASIC\n"
        f"set tpa_speed_basic_delay = {round(tpa_delay * 1000)}\n"
        f"set tpa_speed_basic_gravity = {round(tpa_gravity * 100)}\n"
        #f"set tpa_speed_max_voltage = {round(max_voltage * 100)}\n"
        f"set tpa_speed_pitch_offset = {round(pitch_offset_basic * 10)}\n"
        f"#========================================\n"
        f"set tpa_speed_type = ADVANCED\n"
        f"set tpa_speed_adv_mass = {round(mass * 1000)}\n"
        f"set tpa_speed_adv_drag_k = {round(drag_k * 10000)}\n"
        f"set tpa_speed_adv_thrust = {round(thrust * 1000)}\n"
        f"set tpa_speed_adv_prop_pitch = {round(prop_pitch * 100)}\n"
        f"set motor_kv = {round(motor_kv)}\n"
        #f"set tpa_speed_max_voltage = {round(max_voltage * 100)}\n"
        f"set tpa_speed_pitch_offset = {round(pitch_offset_advanced * 10)}\n"
        f"#========================================\n"
        f"set tpa_speed_type = AERODYNAMICS\n"
        f"mass = {mass}\n"
        f"set tpa_speed_adv_thrust = {round(thrust_aerodynamics * 1000)}\n"
        f"set tpa_speed_adv_prop_pitch = {round(prop_pitch_aerodynamics * 100)}\n"
        f"lift_zero = {lift_zero}\n"
        f"lift_slope = {lift_slope}\n"
        f"drag_parasitic = {drag_parasitic}\n"
        f"drag_induced = {lift_slope}\n"
        f"#========================================\n"
    )
    print(settings_text)
