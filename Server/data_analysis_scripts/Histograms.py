# code for distribution of durations of games
import matplotlib
import numpy as np

matplotlib.use('TkAgg')
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


import base64

def buffer_to_base64(buf):
    """ Convert a buffer to a base64 encoded string suitable for JSON embedding. """
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def json_get_games_durations(task, percentage):
    durations = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # base_directory = r'C:\Users\ASUS\Desktop\final_project\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
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
    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg')
    buf.seek(0)
    return buffer_to_base64(buf)


# Now call the function with the durations list
# image = create_game_time_distribution('diamond',30)

# image1 = Image.open(image)  # Open the image from the BytesIO buffer
# image1.show()


# code for actions ditribution graphs

def json_get_games_action(task, action, percentage):
    action_freq = {'mines': [],
                   'pick-ups': [],
                   'uses': [],
                   'crafts': [],
                   'physical': []}
    # base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    base_directory = r'C:\Users\ASUS\Desktop\final_project\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    categories = ['mines', 'pick-ups', 'uses', 'crafts', 'physical']
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        for cat in categories:
            try:
                action_freq[cat].append(json_content['distrbution']['actions'][cat][action])
            except:
                if cat == 'physical':
                    continue
                else:
                    action_freq[cat].append(0)
    return action_freq


def create_game_action_distribution(task, action, percentage):
    action_freq = json_get_games_action(task, action, percentage)
    categories = ['mines', 'pick-ups', 'uses', 'crafts', 'physical']
    category_images = {}

    for cat in categories:
        if len(action_freq[cat]) > 0:
            bin_edges = np.linspace(min(action_freq[cat]) - 1, max(action_freq[cat]) + 1, 6)
            plt.hist(action_freq[cat], bins=bin_edges, edgecolor='black', color='#7293cb')
            plt.xlabel('Number of times action was done')
            plt.ylabel('Frequency')
            plt.title('Distribution Graph - Number of Times Players ' + cat + ' of ' + action)
            buf = io.BytesIO()
            plt.savefig(buf, format='jpeg')
            plt.close()  # Make sure to close the plot
            buf.seek(0)
            base64_string = buffer_to_base64(buf)
            if cat not in category_images:
                category_images[cat] = []
            category_images[cat].append(base64_string)

    return category_images  # Returns a dictionary of categories, each containing a list of base64 strings


def create_all_actions_distribution(task, actions, percentage):
    buffers = []
    for action in actions:
        buffers = buffers + create_game_action_distribution(task, action, percentage)        
    return buffers


# example how to call this function
# images = create_all_actions_distribution('diamond',['dirt','granite'],30)
# how to open the buffers array


#     image = Image.open(buf)  # Open the image from the BytesIO buffer
#     image.show()


# distribution for inventory
def json_get_games_item(task, item, percentage):
    item_freq = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
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
    item_freq = json_get_games_item(task, item, percentage)
    bin_edges = np.linspace(min(item_freq) - 1, max(item_freq) + 1, 6)
    plt.hist(item_freq, bins=bin_edges, edgecolor='black', color='#7293cb')

    # Add labels and title
    plt.xlabel('Number of times action was done')
    plt.ylabel('Frequency')
    plt.title('Distribution Graph - Number of ' + item + ' in inventory at the end of the game')
    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg')
    buf.seek(0)
    return [buffer_to_base64(buf)]

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
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
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
    buf = io.BytesIO()
    plt.savefig(buf, format='jpeg')
    buf.seek(0)
    return [buffer_to_base64(buf)]


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

def create_all_game_data_as_json(task, actions, items, keys, percentage):
    data = {
        'game_duration_graph': create_game_time_distribution(task, percentage),
        'actions_graphs': {action: create_game_action_distribution(task, action, percentage) for action in actions},
        'inventory_graphs': {item: create_game_item_distribution(task, item, percentage) for item in items},
        'keys_graphs': {key: create_game_key_distribution(task, key, percentage) for key in keys}
    }
    json_data = json.dumps(data, indent=4)  # Use indent for pretty-printing if desired
    return json_data

import json

def load_json_data(file_path):
    """ Load the JSON file and return the data """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

import io
from PIL import Image
import base64

def base64_to_image(base64_string):
    """ Convert a base64 string to a PIL image """
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    return image


from IPython.display import display


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




def main():
    #what is this part? from ron's code

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--percentage', type=int, default=10, help='Percentage of data to process')
    parser.add_argument('--items', type=str, default=['dirt','grass'], help='Comma-separated list of items')
    
    args = parser.parse_args()
    percentage = args.percentage
    items= args.items

    # game_duration_graph = create_game_time_distribution('diamond',percentage)
    actions_graphs = create_all_actions_distribution('diamond',items,percentage)
    # inventory_graphs = create_all_items_distribution('diamond',['dirt','grass'],30)
    # keys_graphs = create_all_keys_distribution('diamond',['space','w'],30)

    # print(json.dumps({
    #     'actions_graphs': actions_graphs
    # }))

    print(actions_graphs)



if __name__ == "__main__":
    main()

