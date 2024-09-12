from headers import *
from settings import *

def format_seconds(seconds):
    # Convert seconds into hours, minutes, and seconds
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    
    # Format the string with hours, minutes, and seconds
    return f"{hours} hours, {minutes} minutes, {seconds:.2f} seconds"


def calculate_bbx_loop_range(data_dict):
    dt = data_dict['dt']
    total_lines = data_dict["total_lines"]
    step_size = max(1, int(dt_target / dt))
    
    # Find the start index based on time_start
    start_idx = next(i for i, t in enumerate(data_dict[header_time]) if t >= time_start)
    
    # Handle cases where time_stop exceeds the available range
    if time_stop > data_dict[header_time][-1]:
        stop_idx = total_lines - 1  # Include the entire remaining range
    else:
        stop_idx = next(i for i, t in enumerate(data_dict[header_time]) if t > time_stop) - 1
    
    return range(start_idx, stop_idx + 1, step_size)
