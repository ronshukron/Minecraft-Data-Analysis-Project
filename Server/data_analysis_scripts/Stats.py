### code for statistics for all games (average, range etc.)
# code for distribution of durations of games
import matplotlib
import numpy as np
import argparse
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
    # base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join("Parsed_Data", str(percentage))
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
        if 'walk_one_cm' in json_content['distrbution']['actions']['physical'].keys():
            walks.append(json_content['distrbution']['actions']['physical']['walk_one_cm']/100)
        else:
            walks.append(0)
    return walks

def json_get_uses(task, percentage,actions):
    uses = []
    #base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join("Parsed_Data", str(percentage))
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
        uses.append(json_content['stats']['actions']['uses'])
    return uses

def json_get_crafts(task, percentage,actions):
    crafts = []
    # base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    directory = os.path.join("Parsed_Data", str(percentage))
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
        crafts.append(json_content['stats']['actions']['crafts'])
    return crafts

def json_get_mines(task, percentage,actions):
    mines = []
    # base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
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
    dict =  [
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
    

    return dict

    # print(dict)

    # with open('Games_Statistics.json', 'w') as json_file:
    #     json.dump(dict, json_file)

#create_game_statistics()

def main():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--percentage', type=int, default=10, help='Percentage of data to process')
    parser.add_argument('--keys', type=str, default=['a','b'], help='list of keys')
    parser.add_argument('--inventory', type=str, default=['white_tulip','stick,dark_oak_planks','gold_ore','dirt'], help='list of inventory')
    parser.add_argument('--actions', type=str, default=['mines.stone','mines.cobblestone','pick-ups.cobblestone','uses.stone pickaxe'], help='list of actions')

    
    args = parser.parse_args()
    percentage = args.percentage
    keys= args.keys
    inventory= args.inventory
    actions= args.actions

    print(json.dumps({
            'stats': create_game_statistics('Diamonds.json',['a'],['a'],['w'],percentage) ### curently hard coded as diamonds, need to get task as argument!
        }))



if __name__ == "__main__":
    main()
