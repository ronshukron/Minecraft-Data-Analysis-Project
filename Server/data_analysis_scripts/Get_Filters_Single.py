# code for distribution of durations of games
import matplotlib

matplotlib.use('TkAgg')
import json
import os
import argparse

def extract_last_part(s):
    parts = s.split('.')
    return '.'.join(parts[-2:]) if len(parts) > 1 else parts[-1]

def extract_date_time(s):
    parts = s.split('-')
    end = parts[-1].split('.')[0]
    date_time = parts[-2]+'-'+end
    return date_time

def get_filters_single_game(task, name):
    res = {
        'actions': [],
        'inventory': [],
        'keys': []
    }
    filters = {}
    steps = []
    # directory = r'C:\Users\Shira\PycharmProjects\Minecraft-Data-Analysis-Project\Server\Parsed_Data\100'
    # Properly format the path with the percentage
    # directory = os.path.join(base_directory, str(percentage))
    # old:
    # directory = os.path.join("Parsed_Data", str(100))
        # my try:
    base = 'C:\Data'
    actual_task = task.split('.')[0]
    # The file path where you want to save the string

    # Open the file in write mode ('w') and write the string into it

    specific_path = f'\\{actual_task}\\100'
    directory = base+specific_path
    #end of change
    # for filename in os.listdir(directory):
    base = 'merged_run_'
    parsed_name = extract_date_time(name)
    filename = base+parsed_name+'.json'
    filepath = os.path.join(directory, filename)
    # Open the JSON file and load its content
    with open(filepath, 'r') as f:
        json_content = json.load(f)
        for step in json_content['steps']:
            if step[0] != 'physical' and step not in steps:
                steps.append(step)
        for item in json_content['distrbution']['inventory']:
            if item not in res['inventory']:
                res['inventory'].append(item)
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


def main():
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--task', type=str, default='House Building from Scratch Task', help='name of a task')
    parser.add_argument('--gamename', type=str, default='cheeky-cornflower-setter-0b1e4d5c2f70-20220413-211200.jsonl', help='name of a video game')

    
    args = parser.parse_args()
    task = args.task
    gamename= args.gamename
    
    res= get_filters_single_game(task, gamename)

    file_path = f'filters_single.json'

    try:
        with open(file_path, 'w') as json_file:
            json.dump(res, json_file, indent=4)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


if __name__ == "__main__":
    main()
