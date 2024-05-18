import pandas as pd
import json
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt

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
    action_frequencies = pd.DataFrame()
    
    min_time = 0
    max_time = 0
    count = 0
    for item_timeline in aggregated_actions.values():
        if count > 0:
            break
        count += 1
        for timeline in item_timeline.values():
            for pair in timeline:
                time_str, _ = pair
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
            for time_str, count in item_timelines:
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

def plot_action_frequencies(action_frequencies_df, percentage, items):
    plt.figure(figsize=(12, 8))
    
    for action in items:
        plt.plot(action_frequencies_df['time'], action_frequencies_df[action], label=action, marker='o', linestyle='-')
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Frequency')
    plt.title(f'Action Frequencies Over Time - {percentage}% of Data')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    graph_path = f'action_frequencies_{percentage}pct.png'
    plt.savefig(graph_path)
    plt.close()
    return graph_path

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--percentage', type=int, help='Percentage of data to process')
    parser.add_argument('--actions', type=str, help='List of actions')

    args = parser.parse_args()
    percentage = args.percentage
    actions = args.actions.split(',')
    #items = args.items.split(',')

    file_paths = get_files_by_percentage('Parsed_Data', percentage)
    parsed_data = load_parsed_json_data(file_paths)
    aggregated_actions = aggregate_actions(parsed_data)
    action_frequencies_df = calculate_action_frequencies_from_timelines(aggregated_actions, actions)
    
    graph_path = plot_action_frequencies(action_frequencies_df, percentage, actions)
    
    print( json.dumps({
        'actions_points': action_frequencies_df.to_json(orient='records'),
        'actions_path': graph_path
        }) )

if __name__ == "__main__":
    main()
