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

def get_single_game_file(directory_path, game_name):
    specific_dir = os.path.join(directory_path, '100')  # Assuming single game data is in '100'
    file_path = os.path.join(specific_dir, game_name)
    if not file_path.endswith('.json'):
        file_path += '.json'
    logging.info(f"Single game file path: {file_path}")
    if not os.path.exists(file_path):
        raise ValueError(f"File {file_path} does not exist.")
    return [file_path]

def load_parsed_json_data(file_paths):
    all_data = []
    for file_path in file_paths:
        logging.info(f"Loading file: {file_path}")
        with open(file_path, 'r') as file:
            try:
                data = json.loads(file.read())
                logging.info(f"Loaded data: {data}")
                if 'timelines' in data:
                    all_data.append(data['timelines'])
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON in file {file_path}: {e}")
    return all_data

def time_string_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds
    except ValueError:
        logging.error(f"Invalid time string format: {time_str}")
        return 0

def calculate_average_quantities_from_timelines(timelines, items, num_points=10):
    avg_quantities = pd.DataFrame()
    
    min_time = float('inf')
    max_time = 0

    for item_timeline in timelines.values():
        for timeline in item_timeline.values():
            for pair in timeline:
                time_str, _ = pair
                time_value = time_string_to_seconds(time_str)
                if time_value > max_time:
                    max_time = time_value
                if time_value < min_time:
                    min_time = time_value

    if min_time == float('inf'):
        min_time = 0

    logging.info(f"Time range: {min_time} to {max_time}")

    regular_time_points = np.linspace(min_time, max_time, num_points)
    avg_quantities['time'] = regular_time_points

    for item in items:
        item_quantities = [0] * num_points
        for i, time_point in enumerate(regular_time_points):
            quantities_at_time = []
            for timeline in timelines.get('inventory', {}).get(item, []):
                time_str, quantity = timeline
                time_seconds = time_string_to_seconds(time_str)
                if time_seconds <= time_point:
                    quantities_at_time.append(quantity)
            if quantities_at_time:
                item_quantities[i] = np.mean(quantities_at_time)
            else:
                item_quantities[i] = 0
        logging.info(f"Quantities for item {item}: {item_quantities}")
        avg_quantities[item] = item_quantities

    return avg_quantities

def aggregate_timelines(parsed_data):
    aggregated_timelines = {'inventory': {}, 'actions': {}}

    for data in parsed_data:
        for item, timeline in data.get('inventory', {}).items():
            if item not in aggregated_timelines['inventory']:
                aggregated_timelines['inventory'][item] = timeline
            else:
                aggregated_timelines['inventory'][item].extend(timeline)

    logging.info(f"Aggregated timelines: {aggregated_timelines}")
    return aggregated_timelines

def plot_average_quantities(avg_quantities_df, game_name, items):
    plt.figure(figsize=(12, 8))
    
    for item in items:
        if item in avg_quantities_df.columns:
            plt.plot(avg_quantities_df['time'], avg_quantities_df[item], label=item, marker='o', linestyle='-')
            logging.info(f"Plotting item: {item}")
        else:
            logging.warning(f"Data for item {item} is not available in the DataFrame.")
    plt.xlabel('Time (seconds)')
    plt.ylabel('Quantity')
    plt.title(f'Average Quantities Over Time - {game_name}')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph_path = f'inventory_quantities_{game_name}.png'
    plt.savefig(graph_path)
    plt.close()
    return graph_path

def main():
    # Configure logging to a file
    logging.basicConfig(filename='script2.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Process single game inventory data.')
    parser.add_argument('--inventory', type=str, required=True, help='List of inventory items')
    parser.add_argument('--game_name', required=True, help='Specific game file to analyze')
    parser.add_argument('--task', required=True, help='The task type (Diamonds, House_Building_rng, House_Building)')  # Added argument for task

    args = parser.parse_args()
    logging.info(f'Received inventory: {args.inventory}')
    logging.info(f'Received game name: {args.game_name}')
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

    # Parse the inventory string
    inventory = args.inventory.split(',')

    transformed_game_name = transform_game_name(args.game_name)

    file_paths = get_single_game_file(directory, transformed_game_name)  # Pass the determined directory
    logging.info(f'File paths: {file_paths}')
    parsed_data = load_parsed_json_data(file_paths)
    aggregated_timelines = aggregate_timelines(parsed_data)
    avg_quantities_df = calculate_average_quantities_from_timelines(aggregated_timelines, inventory)
    
    graph_path = plot_average_quantities(avg_quantities_df, transformed_game_name, inventory)
    
    logging.info(f"Generated graph at: {graph_path}")
    print(json.dumps({
        'inv_points': avg_quantities_df.to_json(orient='records'),
        'inv_path': graph_path
    }))

if __name__ == "__main__":
    main()
