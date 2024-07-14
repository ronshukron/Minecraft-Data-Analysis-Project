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
    directory = os.path.join("Parsed_Data", str(percentage))

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
    parser.add_argument('--percentage', type=int, default=10, help='Percentage of data to process')

    
    args = parser.parse_args()
    task = args.task
    percentage= args.percentage
    
    res= get_filters(task, percentage)

    file_path = f'filters_dataset.json'

    try:
        with open(file_path, 'w') as json_file:
            json.dump(res, json_file, indent=4)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")


if __name__ == "__main__":
    main()

