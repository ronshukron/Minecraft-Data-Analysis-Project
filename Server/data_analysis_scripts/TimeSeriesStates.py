import pandas as pd
import json
import numpy as np
import os
import argparse
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend
import matplotlib.pyplot as plt
import logging
import re

def transform_game_name(file_path):
    # Regular expression to extract the date and time from the file name
    match = re.search(r'\d{8}-\d{6}', file_path)
    if match:
        # Construct the new file name format
        return f"merged_run_{match.group()}.json"
    else:
        raise ValueError("Invalid file name format.")

def get_files_by_percentage(directory_path, percentage, game_name=None):
    if percentage == 0 and game_name:
        # Handle special case for single game analysis
        specific_dir = os.path.join(directory_path, '100')  # Assuming single game data is in '100'
        file_path = os.path.join(specific_dir, game_name)
        logging.info(f'file_path: {file_path}')

        if not os.path.exists(file_path):
            raise ValueError(f"File {file_path} does not exist.")
        return [file_path]
    else:
        # Normal operation for other percentages
        specific_dir = os.path.join(directory_path, str(percentage))
        if not os.path.exists(specific_dir):
            raise ValueError(f"Directory {specific_dir} does not exist.")
        return [os.path.join(specific_dir, f) for f in os.listdir(specific_dir) if f.endswith('.json')]

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

def calculate_action_frequencies_from_timelines(aggregated_actions, specified_actions, num_points=15):
    action_frequencies = pd.DataFrame()
    
    min_time = 0
    max_time = 0
    count = 0
    # logging.info(f"aggregated_actions.values(): {aggregated_actions.values()}")

    for item_timeline in aggregated_actions.values():
        if count > 0:
            break
        count += 1
        # logging.info(f"item_timeline: {item_timeline}")
        for timeline in item_timeline.values():
            for pair in timeline:
                time_str, _ = pair
                time_value = time_string_to_seconds(time_str)
                if time_value > max_time:
                    max_time = time_value
    regular_time_points = np.linspace(min_time, 900, num_points)
    action_frequencies['time'] = regular_time_points
    
    count = 0
    logging.info(f"specified_actions: {specified_actions}")
    for action in specified_actions:
        p_action = action.replace('_', ' ')
        category, item = p_action.split('.')
        item_timelines = aggregated_actions.get(category, {}).get(item, [])
        action_counts = [0] * num_points

        logging.info(f"category, item: {category}, {item}")
        # logging.info(f"item_timelines: {item_timelines}")

        for i, time_point in enumerate(regular_time_points):
            counts_at_time = []
            for time_str, count in item_timelines:
                time_seconds = sum(x * int(t) for x, t in zip([60, 1], time_str.split(":"))) # time_string_to_seconds(time_str)
                if time_seconds <= time_point and time_seconds > 0:
                    counts_at_time.append(count)
            logging.info(f"time_seconds: {time_point}")
            logging.info(f"time_point: {time_point}")
            logging.info(f"counts_at_time: {counts_at_time}")
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
    # logging.info(f"Aggregated actions: {aggregated_actions}")
    return aggregated_actions

def plot_action_frequencies(action_frequencies_df, percentage, items):
    plt.figure(figsize=(12, 8))
    for action in items:
        if action in action_frequencies_df.columns:
            plt.plot(action_frequencies_df['time'], action_frequencies_df[action], label=action, marker='o', linestyle='-')
            logging.info(f"Plotting action: {action}")
        else:
            logging.warning(f"Data for action {action} is not available in the DataFrame.")
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

def parse_custom_format(data_str):
    pattern = r"\{name:(?P<name>[^,]+),actions:\[(?P<actions>[^\]]+)\]\}"
    matches = re.finditer(pattern, data_str)
    formatted_actions = []

    for match in matches:
        item = match.group('name').strip().replace(" ", "_")  # Remove spaces and format
        actions = match.group('actions').strip().split(',')
        for action in actions:
            action = action.strip()  # Clean action string
            formatted_actions.append(f"{action}.{item}")  # Format as 'action.item'

    return formatted_actions

def main():
    # Configure logging to a file
    logging.basicConfig(filename='script.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--percentage', type=int, help='Percentage of data to process')
    parser.add_argument('--actions', type=str, required=True, help='Custom formatted string of actions')
    parser.add_argument('--game_name', help='Specific game file to analyze', default=None)
    parser.add_argument('--task', required=True, help='The task type (Diamonds, House_Building_rng, House_Building)')  # Added argument for task

    args = parser.parse_args()
    percentage = args.percentage
    logging.info(f'Received actions: {args.actions}')
    logging.info(f'Received task: {args.task}')  # Log the task type

    # Determine the directory based on the task type
    base = 'C:\\Data'
    if args.task == 'Diamonds.json':
        directory = os.path.join(base, 'Diamonds')
    elif args.task == 'House_Building_rng.json':
        directory = os.path.join(base, 'House_Building_rng')
    elif args.task == 'House_Building.json':
        directory = os.path.join(base, 'House_Building')
    else:
        raise ValueError("Invalid task type. Choose from 'Diamonds', 'House_Building_rng', or 'House_Building'.")

    # Parse the custom formatted string
    try:
        if percentage == 0:
            actions_split = args.actions.split(',')
            actions = [action.strip() for action in actions_split]
        else:
            actions = parse_custom_format(args.actions)
        logging.info(f'actions after parse: {actions}')
    except Exception as e:
        logging.error(f"Failed to parse custom formatted actions: {e}")
        raise

    if args.game_name:
        transformed_game_name = transform_game_name(args.game_name)
    else:
        transformed_game_name = None
    
    file_paths = get_files_by_percentage(directory, percentage, transformed_game_name)  # Pass the determined directory
    parsed_data = load_parsed_json_data(file_paths)
    aggregated_actions = aggregate_actions(parsed_data)
    action_frequencies_df = calculate_action_frequencies_from_timelines(aggregated_actions, actions)
    
    graph_path = plot_action_frequencies(action_frequencies_df, percentage, actions)
    
    print(json.dumps({
        'actions_points': action_frequencies_df.to_json(orient='records'),
        'actions_path': graph_path
    }))

if __name__ == "__main__":
    main()
