# main.py

# Import the necessary modules
import matplotlib.pyplot as plt
from csv_reader import read_csv_as_dict
import math
from sim_basic import *
from sim_advanced import *

# Example usage of the function
file_path = 'logs/1.BFL.csv'
data_dict = read_csv_as_dict(file_path)

data_sim_basic = []
data_sim_advanced = []
sim_advanced = Sim_advanced()
sim_basic = Sim_basic()
v_basic = 0
v_advanced = 0
for i in range(data_dict["total_lines"]):
    v_basic = v_basic + sim_basic.get_acceleration(v_basic, data_dict['heading[1]'][i], data_dict['Throttle'][i]) * data_dict['dt']
    v_basic = max(v_basic, 0)
    data_sim_basic.append(v_basic)

    v_advanced = v_advanced + sim_advanced.get_acceleration(v_advanced, data_dict['heading[1]'][i], data_dict['Throttle'][i]) * data_dict['dt']
    v_advanced = max(v_advanced, 0)
    data_sim_advanced.append(v_advanced)


data_time = data_dict['time']  # Time in seconds
data_gps_speed = data_dict['GPS_speed'] # GPS speed values
data_throttle = data_dict['Throttle']  # Throttle values
data_pitch = data_dict['heading[1]'] * 180 / math.pi  # Pitch values

# Create the figure
fig, (ax_gps_speed, ax3) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
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
ax4.plot(data_time, data_pitch, 'b', label='Pitch')  # Plot pitch in blue
ax4.set_ylabel('Pitch', color='blue')
ax4.tick_params(axis='y', colors='blue')
ax4.set_ylim(-100, 100)

# Align the legends
#ax2.legend(loc='upper left')
#ax3.legend(loc='upper right')

# Show the plot
plt.show()
