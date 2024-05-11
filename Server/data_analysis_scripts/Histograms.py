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



def json_get_games_durations(task, percentage):
    durations = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
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
    return buf


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
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
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
    buffers = []
    action_freq = json_get_games_action(task, action, percentage)
    categories = ['mines', 'pick-ups', 'uses', 'crafts', 'physical']
    for cat in categories:
        if len(action_freq[cat])>0:
            bin_edges = np.linspace(min(action_freq[cat]) - 1, max(action_freq[cat]) + 1, 6)
            plt.hist(action_freq[cat], bins=bin_edges, edgecolor='black', color='#7293cb')
            # Add labels and title
            plt.xlabel('Number of times action was done')
            plt.ylabel('Frequency')
            plt.title('Distribution Graph - Number of Times Players ' + cat + ' of ' + action)
            buf = io.BytesIO()
            plt.savefig(buf, format='jpeg')
            buf.seek(0)
            buffers.append(buf)
            #plt.savefig('distribution_action freq.' + cat + ' ' + percentage + '.png')
            # Show the graph
            #plt.show()
    return buffers

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
    return [buf]

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
    return [buf]


def create_all_keys_distribution(task, keys, percentage):
    buffers = []
    for key in keys:
        buffers = buffers + create_game_key_distribution(task, key, percentage)
    return buffers


# Now call the function with the durations list

# image1= create_all_keys_distribution('diamond',['space','w'],30)
# image = Image.open(image1[0])  # Open the image from the BytesIO buffer
# image.show()

def main():
    #what is this part? from ron's code


    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('--percentage', type=int, default=100, help='Percentage of data to process')
    # parser.add_argument('--items', type=str, default='white_tulip,stick,dark_oak_planks,gold_ore,dirt', help='Comma-separated list of items')
    #
    # args = parser.parse_args()
    # percentage = args.percentage
    # items = args.items.split(',')

    game_duration_graph = create_game_time_distribution('diamond',30)
    actions_graphs = create_all_actions_distribution('diamond',['dirt','grass'],30)
    inventory_graphs = create_all_items_distribution('diamond',['dirt','grass'],30)
    keys_graphs = create_all_keys_distribution('diamond',['space','w'],30)

if __name__ == "__main__":
    main()
