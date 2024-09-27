import numpy as np
from headers import *

def find_header_row(file_path, identifier):
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            # Strip any leading/trailing whitespace and quotes from the line
            stripped_line = line.strip().strip('"').strip("'")
            if stripped_line.startswith(identifier):
                return i
    return None

def read_csv_as_dict(file_path):
    identifier = "loopIteration"
    # Find the row where the header starts
    header_row = find_header_row(file_path, identifier)
    
    if header_row is None:
        raise ValueError(f"Header row with identifier '{identifier}' not found in the file.")
    
    # Read the header row to get the column names
    column_names = np.genfromtxt(file_path, delimiter=',', skip_header=header_row, max_rows=1, dtype=str)
    # Strip quotes from column names
    column_names = [name.strip('"').strip("'") for name in column_names]

    data_list = []
    total_lines = sum(1 for _ in open(file_path)) - (header_row + 1)
    
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i <= header_row:
                continue
            data_list.append(np.array(line.strip().split(','), dtype=float))
            
            # Print progress
            if i % 1000 == 0 or i == total_lines + header_row:
                print(f"Reading file: {i - header_row} / {total_lines} rows")
    
    # Convert list of arrays to a numpy array
    data = np.vstack(data_list)

    # Create a dictionary where the keys are column names and the values are arrays of floats
    data_dict = {column_names[i]: data[:, i] for i in range(len(column_names))}

    data_dict[header_gps_speed] = data_dict[header_gps_speed] / 100
    data_dict[header_pitch] = data_dict[header_pitch] * header_pitch_multiplier_to_rad
    data_dict[header_voltage] = data_dict[header_voltage] * header_voltage_multiplier_to_volts

    #motor_columns = [col for col in column_names if col.startswith('motor[')]
    #throttle_values = np.mean([data_dict[col] for col in motor_columns], axis=0)
    #data_dict['Throttle'] = throttle_values / 2048
    data_dict['Throttle'] = data_dict['debug[2]']/1000

    # Adjust the "time" column to start from zero
    time_values = data_dict[header_time]
    data_dict[header_time] = (data_dict[header_time] - data_dict[header_time][0]) / 1e6
    
    # Calculate the average time interval (dt) in seconds
    num_intervals = len(data_dict[header_time]) - 1
    if num_intervals > 0:
        dt = (data_dict[header_time][-1] - data_dict[header_time][0]) / num_intervals
        data_dict["dt"] = dt

    data_dict["total_lines"] = total_lines

    return data_dict
