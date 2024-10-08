import pandas as pd
import json
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
import logging

def get_files_by_percentage(directory_path, percentage):
    specific_dir = os.path.join(directory_path, str(percentage))
    if not os.path.exists(specific_dir):
        raise ValueError(f"Directory {specific_dir} does not exist.")
    all_files = sorted([os.path.join(specific_dir, f) for f in os.listdir(specific_dir) if f.endswith('.json')])
    logging.info(f"Processing {len(all_files)} files from directory: {specific_dir}")
    return all_files

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

def calculate_average_quantities_from_timelines(timelines, items, num_points=15):
    avg_quantities = pd.DataFrame()
    
    min_time = 0
    max_time = 0
    count = 0
    for item_timeline in timelines.values():
        if count > 0:
            break
        count += 1
        for timeline in item_timeline.values():
            for pair in timeline:
                time_str, _ = pair
                time_value = time_string_to_seconds(time_str)
                if time_value > max_time:
                    max_time = time_value

    regular_time_points = np.linspace(min_time, 900, num_points)
    avg_quantities['time'] = regular_time_points

    for item in items:
        item_quantities = [0] * num_points
        for i, time_point in enumerate(regular_time_points):
            quantities_at_time = []
            for timeline in timelines.get('inventory', {}).get(item, []):
                time_str, quantity = timeline
                time_seconds = sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))
                if time_seconds <= time_point:
                    quantities_at_time.append(quantity)
            if quantities_at_time:
                item_quantities[i] = np.mean(quantities_at_time)

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

    return aggregated_timelines

def plot_average_quantities(avg_quantities_df, percentage, items):
    plt.figure(figsize=(12, 8))
    
    for item in items:
        plt.plot(avg_quantities_df['time'], avg_quantities_df[item], label=item, marker='o', linestyle='-')
    
    plt.xlabel('Time (seconds)')
    plt.ylabel('Quantity')
    plt.title(f'Average Quantities Over Time - {percentage}% of Data')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    graph_path = f'inventory_quantities_{percentage}pct.png'
    plt.savefig(graph_path)
    plt.close()
    return graph_path

def main():
    logging.basicConfig(filename='script.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--percentage', type=int, default=100, help='Percentage of data to process')
    parser.add_argument('--inventory', help='List of inventory')
    parser.add_argument('--task', required=True, help='The task type (Diamonds, House_Building_rng, House_Building)')  # Added argument for task

    args = parser.parse_args()
    percentage = args.percentage
    inventory = args.inventory.split(',')
    logging.info(f'Received inventory: {inventory}')
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

    file_paths = get_files_by_percentage(directory, percentage)  # Pass the determined directory
    parsed_data = load_parsed_json_data(file_paths)
    aggregated_timelines = aggregate_timelines(parsed_data)
    avg_quantities_df = calculate_average_quantities_from_timelines(aggregated_timelines, inventory)
    
    graph_path = plot_average_quantities(avg_quantities_df, percentage, inventory)
    
    print(json.dumps({
        'inv_points': avg_quantities_df.to_json(orient='records'),
        'inv_path': graph_path
    }))

if __name__ == "__main__":
    main()
