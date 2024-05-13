### code for statistics for all games (average, range etc.)
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

def json_get_walking_cm(task, percentage,actions):
    walks = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        walks.append(json_content['distrbution']['actions']['physical']['walk_one_cm']/100)
    return walks

def json_get_uses(task, percentage,actions):
    uses = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        uses.append(json_content['stats']['actions']['uses'])
    return uses

def json_get_crafts(task, percentage,actions):
    crafts = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        crafts.append(json_content['stats']['actions']['crafts'])
    return crafts

def json_get_mines(task, percentage,actions):
    mines = []
    base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join(base_directory, str(percentage))
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
        mines.append(json_content['stats']['actions']['mines'])
    return mines

def create_game_statistics(task, actions, items, keys, percentage):
    walks = json_get_walking_cm(task, percentage,actions)
    uses = json_get_uses(task, percentage, actions)
    crafts = json_get_crafts(task,percentage,actions)
    mines = json_get_mines(task, percentage,actions)
    walk_stats = calculate_stats(walks)
    uses_stats = calculate_stats(uses)
    crafts_stats = calculate_stats(crafts)
    mines_stats = calculate_stats(mines)
    dict = {
        'stats': [
            {'name': 'walks',
             'average':walk_stats[0],
             'min':walk_stats[1][0],
             'max':walk_stats[1][1],
             'std_deviation':walk_stats[2]},
            {'name': 'uses',
             'average':uses_stats[0],
             'min':uses_stats[1][0],
             'max':uses_stats[1][1],
             'std_deviation':uses_stats[2]},
            {'name': 'crafts',
             'average':crafts_stats[0],
             'min':crafts_stats[1][0],
             'max':crafts_stats[1][1],
             'std_deviation':crafts_stats[2]},
            {'name': 'mines',
             'average':mines_stats[0],
             'min':mines_stats[1][0],
             'max':mines_stats[1][1],
             'std_deviation':mines_stats[2]},
        ]
    }


    with open('Games_Statistics.json', 'w') as json_file:
        json.dump(dict, json_file)

#create_game_statistics()

def main():
    create_game_statistics('a',['a'],['a'],['w'],100)
if __name__ == "__main__":
    main()
