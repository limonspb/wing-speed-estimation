import numpy as np
import math
from csv_reader import read_csv_as_dict
import settings
from headers import *
from sim_aerodynamics import *
from scipy.optimize import least_squares
import matplotlib.pyplot as plt



def linear_residuals(params, x, y):
    return y - (params[0]*x + params[1]) 

def sq_parabola_residuals(params, x, y):
    return y - params[0] / x**2 

def get_lift_by_aoa_line(data_dict, bbx_loop_range, use_gps_path = True):
    time_all = data_dict[header_time][bbx_loop_range]
    pos_x = data_dict["gpsCartesianCoords[0]"][bbx_loop_range]
    pos_y_all = data_dict["gpsCartesianCoords[1]"][bbx_loop_range]
    pos_z = data_dict["gpsCartesianCoords[2]"][bbx_loop_range]
    gps_speed_all = data_dict[header_gps_speed][bbx_loop_range]
    roll = 57.3 * data_dict[header_roll][bbx_loop_range]
    pitch = -57.3 * data_dict[header_pitch][bbx_loop_range] 
    accel_x = data_dict[header_accel_x][bbx_loop_range]
    accel_z = data_dict[header_accel_z][bbx_loop_range]   
    
    x0 = [1, 0]
    path_line = least_squares(linear_residuals, x0, args=(time_all, pos_y_all))
    print(f"path linear = {path_line.x[0]}*x + {path_line.x[1]}, cost={path_line.cost}")          
    
    if use_gps_path:
        dx = pos_x[1 : -1] - pos_x[0 : -2]
        dy = pos_y_all[1 : -1] - pos_y_all[0 : -2]
        dz = pos_z[1 : -1] - pos_z[0 : -2]
        distance = np.sqrt(dx*dx + dy*dy + dz*dz)
        non_zero_dist = distance > 0                # same gps points filtration
        path_angle = np.asin(dy[non_zero_dist] / distance[non_zero_dist]) * 57.3    #path angle estimation
        roll = roll[0 : -2][non_zero_dist]
        pitch = pitch[0 : -2][non_zero_dist]
        time = time_all[0 : -2][non_zero_dist]
        accel_x = accel_x[0 : -2][non_zero_dist]
        accel_z = accel_z[0 : -2][non_zero_dist]
        data_gps_speed = gps_speed_all[0 : -2][non_zero_dist]
    else:
        path_angle = np.asin(path_line.x[0] / gps_speed_all) * 57.3
        time = time_all
        data_gps_speed = gps_speed_all
          
    angle_of_attack_est = pitch - path_angle    #angle of attack estimation array
    
    data_filter = np.logical_and.reduce([np.abs(roll) < settings.limit_roll,  np.abs(accel_x) < settings.limit_accel_x, accel_z < settings.limit_accel_z_max, accel_z > settings.limit_accel_z_min])
    path_angle = path_angle[data_filter]
    pitch = pitch[data_filter]  
    angle_of_attack_est = angle_of_attack_est[data_filter]
    time = time[data_filter] 
    accel_z = accel_z[data_filter]
    data_gps_speed = data_gps_speed[data_filter] 
       
    sim_aerodynamics = Sim_aerodynamics(settings.prop_max_speed_gain, settings.lift_zero, settings.lift_slope, settings.drag_parasitic, settings.drag_induced)
    lift_force_coefs = np.zeros(data_gps_speed.size)           #lift forces coeffs
    for i in range(lift_force_coefs.size):
        lift_coef = sim_aerodynamics.get_lift_force_coef(data_gps_speed[i], accel_z[i])
        lift_force_coefs[i] = lift_coef
       
    # Create the figure
    fig, (ax_altitude, ax_angles, ax_cl_v, ax_cl_aoa) = plt.subplots(4, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 3, 3, 3]})
    fig.subplots_adjust(right=0.8)   
    
    ax_altitude.set_ylabel('GPS Alt, V', color='r')
    ax_altitude.set_xlabel('t, s', color='r')
    ax_altitude.grid(True)
    ax_altitude.plot(time_all, pos_y_all, label = "altitude")
    ax_altitude.plot(time_all, gps_speed_all, label = "speed")
    ax_altitude.legend(loc='best')  
    
    ax_angles.grid(True)
    ax_angles.plot(data_gps_speed, path_angle, "*", label = "path angle")
    ax_angles.plot(data_gps_speed, pitch, "o", label = "pitch angle")
    ax_angles.plot(data_gps_speed, angle_of_attack_est, "+", label = "angle of attack")
    ax_angles.legend(loc='best')    
      
    x0 = [1]
    cl_v_parabola = least_squares(sq_parabola_residuals, x0, args=(data_gps_speed, lift_force_coefs))    
    min_v = min(data_gps_speed)
    max_v = max(data_gps_speed)
    v_range = np.linspace(min_v, max_v, 500, True)  
    clift_range = cl_v_parabola.x[0] / v_range ** 2
    ax_cl_v.grid(True)
    ax_cl_v.plot(data_gps_speed, lift_force_coefs, "o")
    ax_cl_v.plot(v_range, clift_range)
    
    x0 = [1, 0]
    cl_aoa_line = least_squares(linear_residuals, x0, args=(angle_of_attack_est, lift_force_coefs))
    print(f"lift coefs by angle of attack linear y = {cl_aoa_line.x[0]}*x + {cl_aoa_line.x[1]}, cost={cl_aoa_line.cost}")    
    min_aoa = min(angle_of_attack_est)
    max_aoa = max(angle_of_attack_est)
    aoa_range = np.linspace(min_aoa, max_aoa, 3, True)
    clift_range = cl_aoa_line.x[0] * aoa_range + cl_aoa_line.x[1]
    ax_cl_aoa.grid(True)
    ax_cl_aoa.plot(angle_of_attack_est, lift_force_coefs, "*")
    ax_cl_aoa.plot(aoa_range, clift_range)

    
    plt.show()


    
    