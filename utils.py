from headers import *
from settings import *
import os

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

def select_csv_file(folder_path):
    # Step 2: Scan the folder and subfolders for CSV files
    csv_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.csv'):
                # Store the full path along with the file name
                csv_files.append(os.path.join(root, file))

    # Check if there are CSV files available
    if not csv_files:
        print("No CSV files found in the specified folder or its subfolders.")
        return None

    # Step 3: Print a message to the user
    print("Select a CSV Blackbox file:")

    # List the available files with their relative paths for easier selection
    for idx, file in enumerate(csv_files, start=1):
        # Display the file path relative to the base folder
        relative_path = os.path.relpath(file, folder_path)
        print(f"[{idx}] {relative_path}")

    # Step 4: Ask user to input a number
    while True:
        try:
            selection = int(input("Enter the number of the file you want to select: "))
            if 1 <= selection <= len(csv_files):
                break
            else:
                print("Invalid selection. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Step 5: Print the selected file
    selected_file = csv_files[selection - 1]
    print(f"Selected file: {selected_file}")

    # Step 6: Return the selected file path
    return selected_file