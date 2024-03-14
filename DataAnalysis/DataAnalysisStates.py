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


def calculate_action_frequencies_from_timelines(aggregated_actions, specified_actions, num_points=10):
    # This example assumes each timeline entry is a dict with item names as keys and lists of [time, quantity] pairs as values
    # Initialize a DataFrame to store the new time points and average quantities
    action_frequencies = pd.DataFrame()
    
    # Example of converting timeline times to seconds and aggregating quantities
    # This part needs to be adapted based on the exact structure of your timelines
    min_time = 0  # Assuming time starts at 0
    max_time = 0
    count = 0
    for item_timeline in aggregated_actions.values():
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
    

    for action in specified_actions:
        category, item = action.split('.')
        item_timelines = aggregated_actions.get(category, {}).get(item, [])
        action_counts = [0] * num_points

        for i, time_point in enumerate(regular_time_points):
            counts_at_time = []
            my_count = 0
            for time_str, count in item_timelines:
                my_count+=1
                time_seconds = time_string_to_seconds(time_str)
                if time_seconds <= time_point and time_seconds > 0: 
                    counts_at_time.append(count)
            action_counts[i] = np.mean(counts_at_time)

        action_frequencies[action] = action_counts

    return action_frequencies


def aggregate_actions(parsed_data):
    aggregated_actions = {}

    for data in parsed_data:
        actions_data = data.get('actions', {})
        for action_category, items in actions_data.items():
            if action_category not in aggregated_actions:
                aggregated_actions[action_category] = {}
            for item, timelines in items.items():
                if item not in aggregated_actions[action_category]:
                    aggregated_actions[action_category][item] = timelines
                else:
                    aggregated_actions[action_category][item].extend(timelines)

    return aggregated_actions

def plot_action_frequencies(action_frequencies_df, percentage):
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
    plt.savefig(f'D:\\University_Studies\\Project\\Graphs\\action_frequencies_{percentage}pct.png')
    plt.close()





percentage = 100  # Example: Process and plot for 10% of the data

# Get the file paths for the specified percentage of data
file_paths = get_files_by_percentage('D:\\University_Studies\\Project\\Parsed_Data', percentage)

# Load and aggregate actions from the selected files
parsed_data = load_parsed_json_data(file_paths)
aggregated_actions = aggregate_actions(parsed_data)  # Assuming this function is already correctly implemented

# Specify the actions you're interested in analyzing
specified_actions = ["mines.stone", "mines.cobblestone", "pick-ups.cobblestone", "uses.stone pickaxe"]

# Calculate action frequencies over time
action_frequencies_df = calculate_action_frequencies_from_timelines(aggregated_actions, specified_actions)

# Plot the action frequencies over time and save the graph
plot_action_frequencies(action_frequencies_df, percentage)




