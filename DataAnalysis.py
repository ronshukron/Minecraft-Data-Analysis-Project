import pandas as pd
import matplotlib.pyplot as plt
import json
import glob  # Import glob module

# Function to load JSONL files from a directory, concatenate them into a single DataFrame, and adjust time
def load_jsonl_files_from_dir(directory_path):
    data_frames = []
    # Use glob to find all JSONL files in the directory
    file_paths = glob.glob(directory_path + '/*.jsonl')
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = [json.loads(line) for line in file]
            temp_df = pd.DataFrame(data)
            # Subtract the first timestamp from all timestamps to start from 0
            temp_df['adjusted_milli'] = temp_df['milli'] - temp_df['milli'].iloc[0]
            data_frames.append(temp_df)
    return pd.concat(data_frames, ignore_index=True)


# Function to parse inventory data and track changes over time
def parse_inventory_changes(df):
    inventory_over_time = {}
    
    for index, row in df.iterrows():
        current_inventory = {item['type']: item['quantity'] for item in row['inventory']}
        
        for item_type, quantity in current_inventory.items():
            if item_type not in inventory_over_time:
                inventory_over_time[item_type] = [0] * (index + 1)
            inventory_over_time[item_type].extend([quantity] * (1 + index - len(inventory_over_time[item_type])))
        
        for item_type, quantities in inventory_over_time.items():
            if item_type not in current_inventory:
                inventory_over_time[item_type].append(quantities[-1])

    for item_type, quantities in inventory_over_time.items():
        if len(quantities) < len(df):
            inventory_over_time[item_type].extend([quantities[-1]] * (len(df) - len(quantities)))
    
    return pd.DataFrame(inventory_over_time)

# Specify the directory path that contains your JSONL files
directory_path = r"D:\University_Studies\Project\Task_10_only_json_test_100_merged"

# Load JSONL files from the specified directory and adjust time
df = load_jsonl_files_from_dir(directory_path)

print(df)

# Parse inventory changes
inventory_df = parse_inventory_changes(df)
print(inventory_df)
# Plotting function for multiple items with adjusted time on x-axis
def plot_inventory_changes(inventory_df, df_time, *item_names):
    plt.figure(figsize=(10, 6))
    for item_name in item_names:
        if item_name in inventory_df.columns:
            plt.plot(df_time / 1000, inventory_df[item_name], label=item_name)  # Convert milliseconds to seconds
        else:
            print(f'Item {item_name} not found in inventory data.')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Quantity')
    plt.title('Inventory Changes Over Time')
    plt.legend()
    plt.show()

# Example: Plot inventory changes for multiple items with adjusted time on x-axis
plot_inventory_changes(inventory_df, df['adjusted_milli'], 'wooden_axe', 'oak_log', 'dark_oak_planks') #dark_oak_planks
