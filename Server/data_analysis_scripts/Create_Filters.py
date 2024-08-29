# code for distribution of durations of games
import matplotlib

matplotlib.use('TkAgg')
import json
import os
import argparse

def extract_last_part(s):
    parts = s.split('.')
    return '.'.join(parts[-2:]) if len(parts) > 1 else parts[-1]

def get_filters(task, percentage):
    res = {
        'actions': [],
        'inventory': [],
        'keys': []
    }
    filters = {}
    steps = []
    # base_directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data'
    # Properly format the path with the percentage
    # directory = os.path.join(base_directory, str(percentage))
    # old code
    directory = os.path.join("Parsed_Data", str(percentage))
    # my try:
    base = 'C:\\Data'
    actual_task = task.split('.')[0]
    specific_path = f'\\{actual_task}\\{percentage}'
    directory = base+specific_path
    #end of change
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # Open the JSON file and load its content
        with open(filepath, 'r') as f:
            json_content = json.load(f)
            for step in json_content['steps']:
                if step[0] != 'physical' and step not in steps:
                    steps.append(step)
            for item in json_content['distrbution']['inventory']:
                if item not in res['inventory']:
                    res['inventory'].append(item.replace('_', ' '))
            for key in json_content['distrbution']['keyboard']:
                if extract_last_part(key) not in res['keys']:
                    res['keys'].append(extract_last_part(key))
                    # print(i)
    # steps_unique = set(steps)
    for step in steps:
        if step[1] in filters.keys() and step[0] not in filters[step[1]]:
            filters[step[1]].append(step[0])
        elif step[1] not in filters.keys():
            filters[step[1]] = [step[0]]

    actions_res = []
    for item in filters.keys():
        temp = {}
        temp['name'] = item
        temp['actions'] = filters[item]
        actions_res.append(temp)

    res['actions'] = actions_res

    return res

def run():
    for task in ['House_Building_rng', 'House_Building', 'Diamonds']:
        for percentage in ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']:
            res = get_filters(task, percentage)
            if not res['actions'] and not res['inventory'] and not res['keys']:
                continue  # Skip saving if no data is found
            
            base = r'C:\Data\Filters'  # Use a raw string for the base path
            specific_path = os.path.join(base, task, percentage)
            
            # Create the directory if it doesn't exist
            os.makedirs(specific_path, exist_ok=True)
            
            file_path = os.path.join(specific_path, 'filters_dataset.json')
            
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(res, json_file, indent=4)
            except Exception as e:
                print(f"Error writing to {file_path}: {e}")

if __name__ == "__main__":
    run()