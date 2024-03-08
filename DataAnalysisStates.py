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


def calculate_action_frequencies_from_timelines(timelines, actions, num_points=10):
    # This example assumes each timeline entry is a dict with item names as keys and lists of [time, quantity] pairs as values
    # Initialize a DataFrame to store the new time points and average quantities
    action_frequencies = pd.DataFrame()
    
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
    action_frequencies['time'] = regular_time_points
    
    for action in actions:
        action_counts = [0] * num_points  # Initialize with zeros to ensure correct length
        for i, time_point in enumerate(regular_time_points):
            counts_at_time = []
            # Assuming timelines for each action are structured as a list of [time_str, count] pairs
            for timeline in timelines.get('actions', {}).get(action, []):
                time_str, count = timeline
                time_seconds = time_string_to_seconds(time_str)
                if time_seconds <= time_point:
                    counts_at_time.append(count)
            if counts_at_time:
                action_counts[i] = np.sum(counts_at_time)  # Sum counts if data is available
            
        action_frequencies[action] = action_counts  # This should now always match the length of index
    
    return action_frequencies


def aggregate_actions(parsed_data):
    aggregated_timelines = {'actions': {}, 'inventory': {}}
    for data in parsed_data:
        for item, timeline in data.get('actions', {}).items():
            item_name, time_Arr = timeline.values()
            if item not in aggregated_timelines['actions']:
                aggregated_timelines['actions'][item] = timeline
            else:
                aggregated_timelines['actions'][item].extend(timeline)

    
    return aggregated_timelines




def plot_action_counts(aggregated_actions):
    plt.figure(figsize=(10, 6))
    actions, counts = zip(*aggregated_actions.items())  # Unpack actions and their counts
    plt.bar(actions, counts, color='skyblue')
    plt.xlabel('Action')
    plt.ylabel('Total Count')
    plt.title('Total Counts of Actions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




# Load parsed data
directory_path = r'D:\University_Studies\Project\Parsed_Data'
parsed_data = load_parsed_json_data(directory_path)

# Assuming you aggregate or otherwise process the loaded data into a single 'timelines' dict
# This step depends on how you want to handle multiple files and aggregate their data
# For simplicity, let's assume we have a single 'timelines' dict to work with
# timelines = parsed_data[0]  # Simplified assumption, you'll likely need to aggregate data from multiple files


parsed_data = load_parsed_json_data(directory_path)
aggregated_timelines = aggregate_actions(parsed_data)  # Aggregate data if necessary

# Specify the actions you're interested in analyzing
actions = ['walk one cm', 'sprint one cm', 'jump', 'fly one cm']  # Example actions

# Calculate action frequencies over time
action_frequencies_df = calculate_action_frequencies_from_timelines(aggregated_timelines, actions)

# Plot the action frequencies over time
plot_action_counts(action_frequencies_df)  # You might adjust this function for action frequencies



