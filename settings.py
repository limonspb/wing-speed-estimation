import math

# change this between True/False if you need to run automatic parameters finding
calculate = True

# user defined parameters
max_voltage = 25.2 # volts
mass = 1.1 # kilograms
motor_kv = 1960

# modify these, if you have a weird plane (usually don't need to modify)
range_delay = (0.1, 10)
range_gravity = (0.1, 10) 

range_twr = (2,10)
range_pitch = (1, 15)
range_drag_k = (0.001, 0.04)

# parameters to plot with, when automatic parameters finding is False (OFF)
prop_pitch = 3.7
drag_k = 0.005
twr = 2

tpa_delay = 1
tpa_gravity = 0.5

dt_target = 0.01
time_start = 0
time_stop = 215

def print_cli_settings():
    print("")
    print("#========================================")
    print("set tpa_speed_est_type = BASIC")
    print(f"set tpa_speed_est_basic_delay = {round(tpa_delay * 1000)}")
    print(f"set tpa_speed_est_basic_gravity = {round(tpa_gravity * 100)}")    
    print(f"set tpa_speed_est_max_voltage  = {round(max_voltage * 100)}")
    print("#========================================")
    print("set tpa_speed_est_type = ADVANCED")
    print(f"set tpa_speed_est_adv_mass = {round(mass * 1000)}")
    print(f"set tpa_speed_est_adv_drag_k = {round(drag_k * 10000)}")
    print(f"set tpa_speed_est_adv_twr = {round(twr * 100)}")
    print(f"set tpa_speed_est_adv_prop_pitch = {round(prop_pitch * 100)}")
    print(f"set motor_kv = {round(motor_kv)}")
    print(f"set tpa_speed_est_max_voltage  = {round(max_voltage * 100)}")
    print("#========================================")
    print("")
    