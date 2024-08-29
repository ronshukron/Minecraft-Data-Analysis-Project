# code for distribution of durations of games
import zipfile
import matplotlib
import numpy as np
#matplotlib.use('TkAgg')
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt
import os
import io
from PIL import Image
from IPython.display import display
import argparse
import base64
import shutil


def buffer_to_base64(buf):
    """ Convert a buffer to a base64 encoded string suitable for JSON embedding. """
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def json_get_games_durations(task, percentage):
    durations = []
    # Properly format the path with the percentage
    #directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data\100'
        # code before change:
    # directory = os.path.join("Parsed_Data", str(percentage))
    # my try:
    base = 'C:\Data'
    actual_task = task.split('.')[0]
    specific_path = f'\{actual_task}\{percentage}'
    directory = base+specific_path
    #end of change
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        if json_content['stats']['time'][0]!='-' and int(json_content['stats']['time'].split(':')[0])<30:
            durations.append(json_content['stats']['time'])
    return durations


def convert_to_minutes(durations):
    # This will hold the converted durations in minutes
    total_minutes_list = []
    for duration in durations:
        minutes, seconds = duration.split(':')
        total_minutes = int(minutes) + int(seconds) / 60
        total_minutes_list.append(total_minutes)
    return total_minutes_list


def create_game_time_distribution(task, percentage):
    durations = json_get_games_durations(task, percentage)
    # Convert durations to minutes
    minutes_list = convert_to_minutes(durations)
    # Now create a histogram with the numerical data
    bin_edges = np.linspace(min(minutes_list) - 1, max(minutes_list) + 1, 6)
    plt.hist(minutes_list, bins=bin_edges, edgecolor='black', color='#7293cb')

    # Add labels and title
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Frequency')
    plt.title('Distribution Graph - Game Duration')

    output_dir='Histo_Results'
    os.makedirs(output_dir, exist_ok=True)
    graph_path = os.path.join(output_dir, f'game_time_histo_{percentage}.png')
    plt.savefig(graph_path)
    plt.close()
    return graph_path


# Now call the function with the durations list
# image = create_game_time_distribution('diamond',30)
# image1 = Image.open(image)  # Open the image from the BytesIO buffer
# image1.show()


# code for actions ditribution graphs
def json_get_games_action(task, action_dict, percentage):
    # action_freq = {'mines': [],
    #                'pick-ups': [],
    #                'uses': [],
    #                'crafts': [],
    #                'physical': []}

    name = action_dict['name']
    categories = action_dict['actions']
    action_freq = {}
    for cat in categories:
        action_freq[cat] = []
# Properly format the path with the percentage
    #directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data\100'
    directory = os.path.join("Parsed_Data", str(percentage))
    # categories = ['mines', 'pick-ups', 'uses', 'crafts', 'physical']
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        for cat in categories:
            try:
                action_freq[cat].append(json_content['distrbution']['actions'][cat][name])
            except:
                if cat == 'physical':
                    continue
                else:
                    action_freq[cat].append(0)
    return action_freq


def create_game_action_distribution(task, action_dict, percentage):
    action_freq = json_get_games_action(task, action_dict, percentage)
    categories = action_dict['actions']#['mines', 'pick-ups', 'uses', 'crafts', 'physical']
    name = action_dict['name']
    clean_name = action_dict['name'].replace('_', ' ')
    category_images = {}

    for cat in categories:
        if len(action_freq[cat]) > 0:
            bin_edges = np.linspace(min(action_freq[cat]) - 1, max(action_freq[cat]) + 1, 6)
            plt.hist(action_freq[cat], bins=bin_edges, edgecolor='black', color='#7293cb')
            plt.xlabel('Number of times action was done')
            plt.ylabel('Frequency')
            plt.title('Distribution Graph - Number of Times Players ' + cat + ' of ' + clean_name)

            output_dir = 'Histo_Results'
            os.makedirs(output_dir, exist_ok=True)
            graph_path = os.path.join(output_dir,f'game_action_histo_{cat}_{name}_{percentage}.png')
            plt.savefig(graph_path)
            plt.close()

            if cat not in category_images:
                category_images[cat] = []
            category_images[cat].append(graph_path)

    return category_images  # Returns a dictionary of categories, each containing a list of base64 strings


def create_all_actions_distribution(task, actions, percentage):
    buffers = []
    for action in actions:
        buffers.append(create_game_action_distribution(task, action, percentage))  
    return buffers


# example how to call this function
# images = create_all_actions_distribution('diamond',['dirt','granite'],30)
# how to open the buffers array
#     image = Image.open(buf)  # Open the image from the BytesIO buffer
#     image.show()


# distribution for inventory
def json_get_games_item(task, item, percentage):
    item_freq = []
    # Properly format the path with the percentage
    # directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data\100'
    # code before change:
    # directory = os.path.join("Parsed_Data", str(percentage))
    # my try:
    base = 'C:\Data'
    actual_task = task.split('.')[0]
    specific_path = f'\{actual_task}\{percentage}'
    directory = base+specific_path
    #end of change
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        try:
            item_freq.append(json_content['distrbution']['inventory'][item])
        except:
            item_freq.append(0)
    return item_freq


def create_game_item_distribution(task, item, percentage):
    filename = "tests.txt"

# Save the string to the text file
    with open(filename, 'w') as file:
        file.write(item)
    item_freq = json_get_games_item(task, item, percentage)
    clean_name = item.replace('_', ' ')
    bin_edges = np.linspace(min(item_freq) - 1, max(item_freq) + 1, 6)
    plt.hist(item_freq, bins=bin_edges, edgecolor='black', color='#7293cb')

    # Add labels and title
    plt.xlabel('Number of times action was done')
    plt.ylabel('Frequency')
    plt.title('Distribution Graph - Number of ' + clean_name + ' in inventory at the end of the game')

    output_dir='Histo_Results'
    os.makedirs(output_dir, exist_ok=True)
    graph_path = os.path.join(output_dir, f'game_item_histo_{item}_{percentage}pct.png')
    plt.savefig(graph_path)
    plt.close()
    return [graph_path]

def create_all_items_distribution(task, items, percentage):
    buffers = []
    for item in items:
        buffers = buffers + create_game_item_distribution(task, item, percentage)
    return buffers


# Now call the function with the durations list
# image1= create_all_items_distribution('diamond',['leather','dirt'],30)
# image = Image.open(image1[1])  # Open the image from the BytesIO buffer
# image.show()
# create a distribution graph for a single key


def json_get_games_key(task, key, percentage):
    key_freq = []
    # Properly format the path with the percentage
    #directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data\100'
    # code before change:
    # directory = os.path.join("Parsed_Data", str(percentage))
    # my try:
    base = 'C:\Data'
    actual_task = task.split('.')[0]
    specific_path = f'\{actual_task}\{percentage}'
    directory = base+specific_path
    #end of change
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        try:
            actual_key = 'key.keyboard.' + key
            key_freq.append(json_content['distrbution']['keyboard'][actual_key])
        except:
            key_freq.append(0)
    return key_freq


def create_game_key_distribution(task, key, percentage):
    key_freq = json_get_games_key(task, key, percentage)
    bin_edges = np.linspace(min(key_freq) - 1, max(key_freq) + 1, 6)
    plt.hist(key_freq, bins=bin_edges, edgecolor='black', color='#7293cb')

    # Add labels and title
    plt.xlabel('Number of times action was done')
    plt.ylabel('Frequency')
    plt.title('Distribution Graph - Number of time the ' + key + ' was used during the game')

    output_dir='Histo_Results'
    os.makedirs(output_dir, exist_ok=True)
    graph_path = os.path.join(output_dir, f'game_key_histo_{key}_{percentage}.png')
    plt.savefig(graph_path)
    plt.savefig(graph_path)
    plt.close()
    return [graph_path]


def create_all_keys_distribution(task, keys, percentage):
    buffers = []
    for key in keys:
        buffers = buffers + create_game_key_distribution(task, key, percentage)
    return buffers


# Now call the function with the durations list
# image1= create_all_keys_distribution('diamond',['space','w'],30)
# image = Image.open(image1[0])  # Open the image from the BytesIO buffer
# image.show()

import json

def create_all_game_data(task, actions, items, keys, percentage):
    items_edited = items.split(',')
    edited_keys = keys.split(',')

    data = {
        'game_duration_graph': create_game_time_distribution(task, percentage),
        'actions_graphs': {action_dict['name']: create_game_action_distribution(task, action_dict, percentage) for action_dict in actions},
        'inventory_graphs': {item: create_game_item_distribution(task, item, percentage) for item in items_edited},
        'keys_graphs': {key: create_game_key_distribution(task, key, percentage) for key in edited_keys}
    }

    json_data = json.dumps(data, indent=4) 
    return json_data


def load_json_data(file_path):
    """ Load the JSON file and return the data """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def base64_to_image(base64_string):
    """ Convert a base64 string to a PIL image """
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image


def display_images_from_json(file_path):
    data = load_json_data(file_path)

    # Handle single game duration graph
    if 'game_duration_graph' in data and data['game_duration_graph']:
        image = base64_to_image(data['game_duration_graph'])
        image.show()

    # Handle categories that may contain multiple images
    for category_name, category_data in data.items():
        if category_name != 'game_duration_graph':  # Skip the single graph we already handled
            for action_item, images_base64 in category_data.items():
                for img_base64 in images_base64:
                    if category_name=='actions_graphs':
                        if len(images_base64[img_base64])>1:
                            print('its happening')
                        image = base64_to_image(images_base64[img_base64][0])
                    else:
                        image = base64_to_image(images_base64[0])
                    print(f"{category_name} - {action_item}")
                    image.show()


def create_zip_with_json(data, filename="game_data.zip"):
    # Create a BytesIO object to hold the ZIP file
    memory_file = io.BytesIO()

    # Create a ZIP file
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Write the JSON data to a file within the ZIP file
        zf.writestr('game_data.json', data)

    # Prepare the ZIP file for sending
    memory_file.seek(0)

    return memory_file

def delete_all_files_in_directory(directory_path):
    """Delete all files in the specified directory."""
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # Iterate over the files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            # Check if it's a file and remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def main():
    # json_output = create_all_game_data(
    #     'diamond',
    #     [{'name':'stone', 'actions':['mines']},{"name":"dark_oak_log","actions":["mines"]},{"name":"crafting table","actions":["pick-ups"]}],
    #     ['dirt', 'grass', 'crafting_table'],
    #     ['space', 'w'],
    #     100
    # )

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--task', type=str, default='diamond')
    parser.add_argument('--percentage', type=int, default=10, help='Percentage of data to process')
    parser.add_argument('--keys', type=str, default=['a','b'], help='list of keys')
    parser.add_argument('--inventory', type=str, default='white_tulip, stick, dark_oak_planks, gold_ore, dirt', help='list of inventory')
    parser.add_argument('--actions', type=str, default='mines.stone, mines.cobblestone, pick-ups.cobblestone, uses.stone', help='list of actions')
    
    args = parser.parse_args()
    task = args.task
    percentage = args.percentage
    keys= args.keys
    inventory = args.inventory
    actions = json.loads(args.actions)
    
    # inventory = args.inventory.split(',')
    # actions = args.actions.split(',')

    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, 'Histo_Results')
    delete_all_files_in_directory(full_path)
    
    json_output= create_all_game_data(
            task,
            actions,
            inventory,
            keys,
            percentage
        )

    # Create a ZIP file containing the JSON data
    zip_memory_file = create_zip_with_json(json_output)
    zip_file_path = 'histograms.zip'  # Modify this path as needed

    # Save the ZIP file to disk
    with open(zip_file_path, 'wb') as f:
        # zip_memory_file.getvalue() gets the entire content of the BytesIO object
        f.write(zip_memory_file.getvalue())

    print(f"ZIP file saved to {zip_file_path}")

if __name__ == "__main__":
    main()

