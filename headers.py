import math

header_roll = "debug[1]"
header_pitch = "debug[2]"
header_throttle = "debug[3]"
header_gps_speed = "GPS_speed"
header_time = "time"
header_voltage = "vbatLatest"

header_pitch_multiplier_to_rad = math.pi/180 / 10
header_voltage_multiplier_to_volts = 1/100

# data for aerodynamics calculate
header_accel_x = "accSmooth[0]"
header_accel_y = "accSmooth[1]"
header_accel_z = "accSmooth[2]"
header_const_plane_mass = "plane_mass"
header_const_wing_load = "wing_load"
header_const_air_density = "air_density"
