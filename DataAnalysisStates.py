import pandas as pd
import matplotlib.pyplot as plt
import json
import glob
import numpy as np

def load_jsonl_files_and_adjust_time(directory_path):
    all_data = []
    for file_path in sorted(glob.glob(directory_path + '/*.jsonl')):
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            df = pd.DataFrame(data)
            df['time'] = (df['milli'] - df['milli'].iloc[0]) / 1000
            if (df['time'] < 0).any():
                print(f"Negative time values found in {file_path}")
                # Print the negative time values
                print(df.loc[df['time'] < 0, 'time'])
                continue
            all_data.append(df)
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

def calculate_average_stats_fixed_points(df, items, num_points=10):
    # Initialize a DataFrame to store the new time points and average quantities
    avg_quantities = pd.DataFrame()
    
    # Create a regular grid of time points from the minimum to the maximum time in the dataset
    min_time = df['time'].min()
    max_time = df['time'].max()
    regular_time_points = np.linspace(min_time, max_time, num_points)
    
    avg_quantities['time'] = regular_time_points
    
    # Explode the inventory lists to rows to facilitate easier aggregation
    df_exploded = df.explode('stats')
    
    # Convert each inventory dict to a Series, then concatenate to the original DataFrame
    inventory_details = df_exploded['stats'].apply(pd.Series)
    df_detailed = pd.concat([df_exploded.drop('stats', axis=1), inventory_details], axis=1)
    
    for item in items:
        item_quantities = []
        for time_point in regular_time_points:
            # Filter for entries close to the current time point and for the specific item
            filtered_df = df_detailed[(df_detailed['time'] <= time_point) & (df_detailed['type'] == item)]
            
            # If there are no entries for this item at this time, carry forward the last known average
            if filtered_df.empty:
                avg_quantity = item_quantities[-1] if item_quantities else 0  # Default to 0 if no previous data
            else:
                avg_quantity = filtered_df['quantity'].mean()
            
            item_quantities.append(avg_quantity)
        
        avg_quantities[item] = item_quantities
    
    return avg_quantities


def plot_average_stats(avg_stats_df):
    plt.figure(figsize=(10, 6))
    line_styles = ['-', '--', '-.', ':']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i, column in enumerate(avg_stats_df.columns[1:]):  # Skip the 'time' column
        line_style = line_styles[i % len(line_styles)]
        color = colors[i % len(colors)]
        plt.plot(avg_stats_df['time'], avg_stats_df[column], label=column, linestyle=line_style, color=color, linewidth=2.5, alpha=1)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Average Value')
    plt.title('Average Value of Stats Over Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Directory containing JSONL files
directory_path = 'D:\\University_Studies\\Project\\Task_10_only_json_test_100_merged'

# Load and adjust time across all JSONL files
df = load_jsonl_files_and_adjust_time(directory_path)

# Specify the stats keys you're interested in
stats_keys = ['minecraft.custom:minecraft.time_since_rest', 'minecraft.custom:minecraft.play_one_minute', 'minecraft.custom:minecraft.time_since_death']

# Calculate average stats for specified keys
avg_stats_df = calculate_average_stats_fixed_points(df, stats_keys)

# Plot the average stats over time
plot_average_stats(avg_stats_df)

