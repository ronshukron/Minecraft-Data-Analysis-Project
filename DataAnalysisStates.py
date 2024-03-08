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

def plot_action_frequencies(action_frequencies_df):
    plt.figure(figsize=(12, 8))
    for action in action_frequencies_df.columns[1:]:  # Skip the 'time' column
        plt.plot(action_frequencies_df['time'], action_frequencies_df[action], label=action, marker='o', linestyle='-')
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.title('Action Frequencies Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




# Load parsed data
# Load parsed data
directory_path = r'D:\University_Studies\Project\Parsed_Data'
parsed_data = load_parsed_json_data(directory_path)

# Aggregate actions data from parsed JSON files
aggregated_actions = aggregate_actions(parsed_data)

# Specify the actions you're interested in analyzing
specified_actions = [ "mines.stone", "mines.cobblestone", "mines.white tulip", "pick-ups.cobblestone", "pick-ups.poppy", "uses.wooden pickaxe", "uses.stone pickaxe", "physical.water one cm", "crafts.dark oak planks", "crafts.wooden pickaxe"]

# Calculate action frequencies over time
action_frequencies_df = calculate_action_frequencies_from_timelines(aggregated_actions, specified_actions)

# Plot the action frequencies over time
# Note: You might need to adjust or create a new plotting function based on the structure of action_frequencies_df

# Plot the action frequencies over time
plot_action_frequencies(action_frequencies_df)



