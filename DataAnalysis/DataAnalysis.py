import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import numpy as np
import os

def get_files_by_percentage(directory_path, percentage):
    all_files = sorted([os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')])
    num_files_to_process = int(len(all_files) * (percentage / 100))
    return all_files[:num_files_to_process]

def load_parsed_json_data(file_paths):
    all_data = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            try:
                data = json.loads(file.read())
                if 'timelines' in data:
                    all_data.append(data['timelines'])
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path}: {e}")
    return all_data


def time_string_to_seconds(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes * 60 + seconds * 1


def calculate_average_quantities_from_timelines(timelines, items, num_points=10):
    # This example assumes each timeline entry is a dict with item names as keys and lists of [time, quantity] pairs as values
    # Initialize a DataFrame to store the new time points and average quantities
    avg_quantities = pd.DataFrame()
    
    # Example of converting timeline times to seconds and aggregating quantities
    # This part needs to be adapted based on the exact structure of your timelines
    min_time = 0  # Assuming time starts at 0
    max_time = 0
    count = 0
    for item_timeline in timelines.values():
        if count > 0:
            break
        count+=1  # Assuming timelines is a dict with items as keys
        for timeline in item_timeline.values():  # Assuming each item has a dict of actions with lists of [time, quantity] pairs
            for pair in timeline:
                time_str, _ = pair  # Assuming pair is a list with [time, quantity]
                time_value = time_string_to_seconds(time_str)
                if time_value > max_time:
                    max_time = time_value
    regular_time_points = np.linspace(min_time, max_time, num_points)
    avg_quantities['time'] = regular_time_points
    
    for item in items:
            item_quantities = [0] * num_points  # Initialize with zeros to ensure correct length
            for i, time_point in enumerate(regular_time_points):
                quantities_at_time = []
                # Assuming timelines for each item are structured as a list of [time_str, quantity] pairs
                for timeline in timelines.get('inventory', {}).get(item, []):
                    time_str, quantity = timeline
                    time_seconds = sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))
                    if time_seconds <= time_point:
                        quantities_at_time.append(quantity)
                if quantities_at_time:
                    item_quantities[i] = np.mean(quantities_at_time)  # Update with actual average if data is available
            
            avg_quantities[item] = item_quantities  # This should now always match the length of index
        
    return avg_quantities


def aggregate_timelines(parsed_data):
    aggregated_timelines = {'inventory': {}, 'actions': {}}
    
    for data in parsed_data:
        # Assuming each 'data' contains a 'timelines' dictionary
        # timelines = data.get('timelines', {})
        
        # Aggregate inventory data
        for item, timeline in data.get('inventory', {}).items():
            if item not in aggregated_timelines['inventory']:
                aggregated_timelines['inventory'][item] = timeline
            else:
                # Assuming timeline is a list of [time, quantity] pairs
                # Extend the existing list with the new one
                aggregated_timelines['inventory'][item].extend(timeline)
                
        # Aggregate actions data (similar approach)
        # You would follow a similar pattern for 'actions' and any other top-level keys in 'timelines'
        # This example focuses on 'inventory' for simplicity
    
    return aggregated_timelines



def plot_inventory_frequencies(action_frequencies_df, percentage):
    plt.figure(figsize=(12, 8))
    for action in action_frequencies_df.columns[1:]:  # Skip the 'time' column
        plt.plot(action_frequencies_df['time'], action_frequencies_df[action], label=action, marker='o', linestyle='-')
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.title(f'Action Frequencies Over Time - {percentage}% of Data')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the figure with the percentage in the filename
    plt.savefig(f'D:\\University_Studies\\Project\\Graphs\\inventory_frequencies_{percentage}pct.png')
    plt.close()






percentage = 100  # Example: Process and plot for 10% of the data

# Get the file paths for the specified percentage of data
file_paths = get_files_by_percentage('D:\\University_Studies\\Project\\Parsed_Data', percentage)

# Load and aggregate actions from the selected files
parsed_data = load_parsed_json_data(file_paths)
aggregated_timelines = aggregate_timelines(parsed_data)

# Calculate average quantities for specified items
items = ['white_tulip', 'stick', 'dark_oak_planks', 'gold_ore', 'dirt']
avg_quantities_df = calculate_average_quantities_from_timelines(aggregated_timelines, items)

# Plot the average quantities over time
plot_inventory_frequencies(avg_quantities_df, percentage)

