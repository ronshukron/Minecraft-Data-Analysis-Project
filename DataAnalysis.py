import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import numpy as np

# Function to load JSONL files from a directory and adjust time
def load_parsed_json_data(directory_path):
    all_data = []
    for file_path in sorted(glob.glob(directory_path + '/*.json')):
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    data = json.loads(line)
                    # Assuming 'timelines' contains the data we're interested in
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



def plot_average_quantities(avg_quantities_df):
    plt.figure(figsize=(10, 6))
    line_styles = ['-', '--', '-.', ':']  # Define a list of line styles
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # Define a list of colors
    for i, column in enumerate(avg_quantities_df.columns[1:]):  # Skip the 'time' column
        # Cycle through line styles and colors
        line_style = line_styles[i % len(line_styles)]
        color = colors[i % len(colors)]
        # Increase linewidth for thicker lines and set alpha to 1 for bolder appearance
        plt.plot(avg_quantities_df['time'], avg_quantities_df[column], label=column, linestyle=line_style, color=color, linewidth=2.5, alpha=1)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Quantity')
    plt.title('Average Quantity of Items Over Time')
    plt.legend()
    plt.grid(True)  # Add grid for better readability
    plt.tight_layout()  # Adjust layout to not cut off labels
    plt.show()



# Load parsed data
directory_path = r'D:\University_Studies\Project\Parsed_Data'
parsed_data = load_parsed_json_data(directory_path)

# Assuming you aggregate or otherwise process the loaded data into a single 'timelines' dict
# This step depends on how you want to handle multiple files and aggregate their data
# For simplicity, let's assume we have a single 'timelines' dict to work with
# timelines = parsed_data[0]  # Simplified assumption, you'll likely need to aggregate data from multiple files


parsed_data = load_parsed_json_data(directory_path)
aggregated_timelines = aggregate_timelines(parsed_data)






# Calculate average quantities for specified items
items = ['white_tulip', 'stick', 'dark_oak_planks', 'gold_ore', 'dirt']
avg_quantities_df = calculate_average_quantities_from_timelines(aggregated_timelines, items)

# Plot the average quantities over time
plot_average_quantities(avg_quantities_df)

