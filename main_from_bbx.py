# main.py

# Import the necessary modules
import matplotlib.pyplot as plt
from csv_reader import read_csv_as_dict
import math
from sim_basic import *
from sim_advanced import *
from scipy.optimize import differential_evolution
from functools import partial
from headers import *


def get_error_sim1(params, data_dict):
    twr, pitch_speed100, drag_coefficient = params
    sim = Sim_advanced(twr, pitch_speed100, drag_coefficient)
    v = 0
    error = 0
    speeds = data_dict[header_gps_speed]
    count = 0
    for i in range(data_dict["total_lines"]):
        v = v + sim.get_acceleration(v, data_dict[header_pitch][i], data_dict['Throttle'][i], data_dict[header_voltage][i]) * data_dict['dt']
        v = max(v, 0)
        d_error = abs(v - speeds[i])
        if not math.isnan(d_error):        
            error = error + d_error
            count = count + 1
        if data_dict[header_time][i] > 215:
            break
    
    return error/count

def get_error_sim2(params, data_dict):
    twr, drag_coefficient = params
    sim = Sim_basic(twr, drag_coefficient)
    v = 0
    error = 0
    speeds = data_dict[header_gps_speed]
    count = 0
    for i in range(data_dict["total_lines"]):
        v = v + sim.get_acceleration(v, data_dict[header_pitch][i], data_dict['Throttle'][i], data_dict[header_voltage][i]) * data_dict['dt']
        v = max(v, 0)
        d_error = abs(v - speeds[i])
        if not math.isnan(d_error):        
            error = error + d_error
            count = count + 1
        if data_dict[header_time][i] > 215:
            break
    
    return error/count



if __name__ == '__main__':

    # Example usage of the function
    file_path = 'logs/1.BFL.csv'
    data_dict = read_csv_as_dict(file_path)

    #test = get_error((4, 73, 0.0045), data_dict=data_dict)
    if False:
        bounds = [(2,10), (40, 100), (0.001, 0.04)]
        get_error_with_data = partial(get_error_sim1, data_dict=data_dict)
        result = differential_evolution(get_error_with_data, bounds, workers=-1)
        optimal_params = result.x
        minimum_value = result.fun
        print("Optimal Parameters:", optimal_params)
        print("Minimum Value:", minimum_value)

    if False:
        bounds = [(2,10), (0.001, 0.05)]
        get_error_with_data = partial(get_error_sim2, data_dict=data_dict)
        result = differential_evolution(get_error_with_data, bounds, workers=-1)
        optimal_params = result.x
        minimum_value = result.fun
        print("Optimal Parameters:", optimal_params)
        print("Minimum Value:", minimum_value)


    data_sim_basic = []
    data_sim_advanced = []
    sim_advanced = Sim_advanced(twr=6.00180600e+00, pitch_speed100=9.83766073e+01, drag_coefficient=5.08622920e-03)
    sim_basic = Sim_basic(twr=3.5729982, drag_coefficient=0.00727245)
    v_basic = 0
    v_advanced = 0
    for i in range(data_dict["total_lines"]):
        v_basic = v_basic + sim_basic.get_acceleration(v_basic, data_dict[header_pitch][i], data_dict['Throttle'][i], data_dict[header_voltage][i]) * data_dict['dt']
        v_basic = max(v_basic, 0)
        data_sim_basic.append(v_basic)

        v_advanced = v_advanced + sim_advanced.get_acceleration(v_advanced, data_dict[header_pitch][i], data_dict['Throttle'][i], data_dict[header_voltage][i]) * data_dict['dt']
        v_advanced = max(v_advanced, 0)
        data_sim_advanced.append(v_advanced)


    data_time = data_dict[header_time]  # Time in seconds
    data_gps_speed = data_dict[header_gps_speed] # GPS speed values
    data_throttle = data_dict['Throttle']  # Throttle values
    data_pitch_degrees = data_dict[header_pitch] * 180 / math.pi  # Pitch values

    # Create the figure
    fig, (ax_gps_speed, ax3) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [7, 3]})
    fig.subplots_adjust(right=0.8)

    # Adjust the space between plots to zero
    plt.subplots_adjust(hspace=0)

    # First plot (GPS Speed over Time)
    line_gps_speed = ax_gps_speed.plot(data_time, data_gps_speed, label='GPS Speed', color='r')[0]
    ax_gps_speed.set_ylabel('GPS Speed', color='r')
    ax_gps_speed.set_title('GPS Speed over Time')
    ax_gps_speed.tick_params(axis='y', labelcolor='r')
    ax_gps_speed.grid(True)

    # Create a secondary y-axis for the simple simulation
    ax_simulation1 = ax_gps_speed.twinx()
    line_simulation1 = ax_simulation1.plot(data_time, data_sim_basic, label='Simple Simulation', color='g')[0]
    ax_simulation1.set_ylabel('Simple Simulation', color='g')
    ax_simulation1.tick_params(axis='y', labelcolor='g')

    ax_simulation2 = ax_gps_speed.twinx()
    ax_simulation2.spines['right'].set_position(('outward', 60))
    line_simulation2 = ax_simulation2.plot(data_time, data_sim_advanced, label='Advanced Simulation', color='b')[0]
    ax_simulation2.set_ylabel('Advanced Simulation', color='b')
    ax_simulation2.tick_params(axis='y', labelcolor='b')

    lines = [line_gps_speed, line_simulation1, line_simulation2]
    labels = [line.get_label() for line in lines]
    ax_gps_speed.legend(lines, labels, loc='upper left')

    # Second plot (Throttle and Pitch over Time)
    ax3.plot(data_time, data_throttle, 'r', label='Throttle')  # Plot throttle in red
    ax3.set_ylabel('Throttle', color='red')
    ax3.tick_params(axis='y', colors='red')
    ax3.grid(True)
    ax3.set_ylim(0, 1.1)

    # Create a second Y-axis on the right for pitch
    ax4 = ax3.twinx()
    ax4.plot(data_time, data_pitch_degrees, 'b', label='Pitch')  # Plot pitch in blue
    ax4.set_ylabel('Pitch', color='blue')
    ax4.tick_params(axis='y', colors='blue')
    ax4.set_ylim(-100, 100)

    # Align the legends
    #ax2.legend(loc='upper left')
    #ax3.legend(loc='upper right')

    # Show the plot
    plt.show()
