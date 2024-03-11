# code for distribution of durations of games
import matplotlib
import numpy as np

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates, timedelta
from datetime import datetime
import pandas as pd
import json
import matplotlib.pyplot as plt
import os


def json_get_games_durations():
    durations = []
    directory = r'C:\Users\Shira\PycharmProjects\MineCraft\Parsed_Data'
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


def create_game_time_distribution():
    durations = json_get_games_durations()
    for i in range(1, 11):
        percentage = i * 0.1
        end_index = int(len(durations) * percentage)
        subset = durations[:end_index]
    # Convert durations to minutes
        minutes_list = convert_to_minutes(subset)
        # Now create a histogram with the numerical data
        bin_edges = np.linspace(min(minutes_list) - 1, max(minutes_list) + 1, 6)
        plt.hist(minutes_list, bins=bin_edges, edgecolor='black', color='#7293cb')

        # Add labels and title
        plt.xlabel('Duration (minutes)')
        plt.ylabel('Frequency')
        plt.title('Distribution Graph')
        plt.savefig('distribution_game_durations' + str(round(i*0.1,1)) + '.png')
        # Show the graph
        #plt.show()


# Now call the function with the durations list
#create_game_time_distribution()

### code for statistics for all games (average, range etc.)

import math

def calculate_stats(numbers):
    if not numbers:
        return None, None, None, None

    # Calculate average
    average = sum(numbers) / len(numbers)

    # Calculate range
    min_val = min(numbers)
    max_val = max(numbers)

    # Calculate standard deviation
    variance = sum((x - average) ** 2 for x in numbers) / len(numbers)
    std_deviation = math.sqrt(variance)

    return round(average), (round(min_val), round(max_val)), round(std_deviation)

def json_get_walking_cm():
    walks = []
    directory = r'C:\Users\Shira\PycharmProjects\MineCraft\Parsed_Data'
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        walks.append(json_content['distrbution']['actions']['physical']['walk_one_cm']/100)
    return walks

def json_get_uses():
    uses = []
    directory = r'C:\Users\Shira\PycharmProjects\MineCraft\Parsed_Data'
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        uses.append(json_content['stats']['actions']['uses'])
    return uses

def json_get_crafts():
    crafts = []
    directory = r'C:\Users\Shira\PycharmProjects\MineCraft\Parsed_Data'
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        crafts.append(json_content['stats']['actions']['crafts'])
    return crafts

def json_get_mines():
    mines = []
    directory = r'C:\Users\Shira\PycharmProjects\MineCraft\Parsed_Data'
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        mines.append(json_content['stats']['actions']['mines'])
    return mines

def create_game_statistics():
    walks = json_get_walking_cm()
    uses = json_get_uses()
    crafts = json_get_crafts()
    mines = json_get_mines()
    dict = {
        10: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        20: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        30: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        40: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        50: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        60: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        70: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        80: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        90: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        },
        100: {
            'walks': [],
            'uses': [],
            'crafts': [],
            'mines': []
        }
    }
    for i in range(1, 11):
        percentage = i * 0.1
        end_index = int(len(walks) * percentage)
        dict[i*10]['walks'] = calculate_stats(walks[:end_index])
        dict[i*10]['uses'] = calculate_stats(uses[:end_index])
        dict[i*10]['crafts'] = calculate_stats(crafts[:end_index])
        dict[i*10]['mines'] = calculate_stats(mines[:end_index])

    with open('Games_Statistics.json', 'w') as json_file:
        json.dump(dict, json_file)

#create_game_statistics()
