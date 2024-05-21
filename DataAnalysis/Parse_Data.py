import json
import os


def convert_millis_to_min_sec(start_millis, current_millis):
    # Calculate the difference in milliseconds
    diff_millis = current_millis - start_millis

    # Convert milliseconds to seconds
    diff_seconds = diff_millis // 1000

    # Calculate minutes and seconds
    minutes = diff_seconds // 60
    seconds = diff_seconds % 60

    # Format as mm:ss
    time_format = f"{minutes:02}:{seconds:02}"

    return time_format


def get_action_type_and_name(action):
    action_name = str(action).split('.')[2].replace('_', ' ')
    if 'mine_block' in action:
        return [action_name, 'mines']
    if 'pickup' in action:
        return [action_name, 'pick-ups']
    if 'use_item' in action:
        return [action_name, 'uses']
    if 'craft_item' in action:
        return [action_name, 'crafts']
    if 'one_cm' in action or 'jump' in action:
        return [action_name, 'physical']

# get keyboard keys count
def get_keyboard_count(data, pars_data):
    for i in range(len(data)):
        if len(data[i]['keyboard']['newKeys']) > 0:
            for key in data[i]['keyboard']['newKeys']:
                if key in pars_data['distrbution']['keyboard']:
                    pars_data['distrbution']['keyboard'][key] += 1
                else:
                    pars_data['distrbution']['keyboard'][key] = 1
    return pars_data


# get actions total count
def get_actions_count(data, pars_data):
    stats = data[len(data) - 1]['stats']
    for key, val in stats.items():
        if 'mine_block' in key:
            subject = str(key).split('.')[2]
            subject.replace('_', ' ')
            pars_data['distrbution']['actions']['mines'][subject] = val
        if 'pickup' in key:
            subject = str(key).split('.')[2]
            subject.replace('_', ' ')
            pars_data['distrbution']['actions']['pick-ups'][subject] = val
        if 'use_item' in key:
            subject = str(key).split('.')[2]
            subject.replace('_', ' ')
            pars_data['distrbution']['actions']['uses'][subject] = val
        if 'craft_item' in key:
            subject = str(key).split('.')[2]
            subject.replace('_', ' ')
            pars_data['distrbution']['actions']['crafts'][subject] = val
        if 'one_cm' in key or 'jump' in key:
            subject = str(key).split('.')[2]
            subject.replace('_', ' ')
            pars_data['distrbution']['actions']['physical'][subject] = val
    return pars_data


# get final inventory
def get_final_inventory(data, pars_data):
    inventory = data[len(data) - 1]['inventory']
    for item in inventory:
        pars_data['distrbution']['inventory'][item['type']] = item['quantity']
    return pars_data


# Timelines
# get inventory progress by time
def get_inventory_timeline(data, pars_data):
    start = data[0]['milli']
    current = {}
    for i in range(len(data)):
        if len(data[i]['inventory']):  # there is something in the inventory at this point of the game
            for item_dict in data[i]['inventory']:  # go over each dict in the inventory
                if item_dict['type'] not in current.keys():
                    pars_data['timelines']['inventory'][item_dict['type']] = [
                        (convert_millis_to_min_sec(start, data[i][
                            'milli']), item_dict['quantity'])]  # first time item in inventory
                    current[item_dict['type']] = item_dict['quantity']
                elif item_dict['quantity'] != current[item_dict['type']]:
                    pars_data['timelines']['inventory'][item_dict['type']].append((convert_millis_to_min_sec(start,
                                                                                                             data[
                                                                                                                 i][
                                                                                                                 'milli']),
                                                                                   item_dict[
                                                                                       'quantity']))  # existing item additional quantity
                    current[item_dict['type']] = item_dict['quantity']
    return pars_data


# get actions progress by time & geenral timeline of action for complex graph
def get_actions_timeline_and_playout(data, pars_data):
    start = data[0]['milli']
    current = {
        'mines': {},
        'pick-ups': {},
        'uses': {},
        'crafts': {},
        'physical': {}
    }
    for i in range(len(data)):
        for key, val in data[i]['stats'].items():
            action = get_action_type_and_name(key)
            if action:
                name = action[0]
                action_type = action[1]
                if name not in current[action_type].keys():
                    # update for timeline graph
                    pars_data['timelines']['actions'][action_type][name] = [
                        (convert_millis_to_min_sec(start, data[i]['milli']), val)]
                    # update for complex actions graph
                    pars_data['steps'].append((action_type, name))
                    # update new amount of action for next iteration
                    current[action_type][name] = val
                elif val != current[action_type][name]:
                    # update for timeline graph
                    pars_data['timelines']['actions'][action_type][name].append(
                        (convert_millis_to_min_sec(start, data[i]['milli']), val))
                    # update for complex actions graph
                    pars_data['steps'].append((action_type, name))
                    # update new amount of action for next iteration
                    current[action_type][name] = val
    return pars_data


# Stats
# check if player was succesfull in finding a diamond pickaxe
def check_diamondaxe(data, pars_data):
    inventory = data[len(data) - 1]['inventory']
    for dict in inventory:
        if dict['type'] == 'diamond_pickaxe' and dict['quantity'] > 0:
            pars_data['stats']['success'] = True
            return pars_data
    return pars_data


# get total game time
def get_game_duration(data, pars_data):
    pars_data['stats']['time'] = convert_millis_to_min_sec(data[0]['milli'], data[len(data) - 1]['milli'])
    return pars_data


# get total uses of each item category
def total_count_of_action_categories(data, pars_data):
    count = {}
    for key, val in data[len(data) - 1]['stats'].items():
        action = get_action_type_and_name(key)
        if action:
            action_type = action[1]
            if action_type not in count.keys():
                count[action_type] = val
            else:
                count[action_type] += val
    for key, val in count.items():
        pars_data['stats']['actions'][key] = val
    return pars_data


# def save_as_json(pars_data, filename):
#     with open(filename.replace('Raw_Data', 'Parsed_Data'), 'w') as f:
#         json.dump(pars_data, f)

def save_as_json(pars_data, filename, output_dir):
    # Extract just the filename and replace 'Raw_Data' with 'Parsed_Data'
    base_filename = os.path.basename(filename).replace('Raw_Data', 'Parsed_Data')
    # Create the full path by joining the output_dir with the base_filename
    output_filename = os.path.join(output_dir, base_filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(output_filename, 'w') as f:
        json.dump(pars_data, f)
    # print(filename)



def parse_game(game_file, filename, output_dir):
    data = []  # will read file into this
    with open(game_file, 'r') as file:  # reading file to the array per line
        for line_number, line in enumerate(file, 1):
            try:
                # Parse the JSON object and append it to the list
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_number} due to JSONDecodeError: {e}")
    # setting dict structure for parsed data
    pars_data = {
        'distrbution': {
            'keyboard': {},
            'actions': {
                'mines': {},
                'pick-ups': {},
                'uses': {},
                'crafts': {},
                'physical': {}
            },
            'inventory': {}
        },
        'timelines': {
            'inventory': {},
            'actions': {
                'mines': {},
                'pick-ups': {},
                'uses': {},
                'crafts': {},
                'physical': {}
            }
        },
        'stats': {
            'success': False,
            'time': 1,
            'actions': {
                'mines': 0,
                'pick-ups': 0,
                'uses': 0,
                'crafts': 0,
                'physical': 0
            }
        },
        'steps': []
    }
    try:
        pars_data = get_keyboard_count(data, pars_data)
        pars_data = get_actions_count(data, pars_data)
        pars_data = get_final_inventory(data, pars_data)
        pars_data = get_inventory_timeline(data, pars_data)
        pars_data = get_actions_timeline_and_playout(data, pars_data)
        pars_data = check_diamondaxe(data, pars_data)
        pars_data = get_game_duration(data, pars_data)
        pars_data = total_count_of_action_categories(data, pars_data)
        save_as_json(pars_data, filename,output_dir)
        print('created succesfully '+filename)
    except:
        print('could parse game '+ filename)


# creating JSON files for parsing all JSONL files in the path
# def parse_all_games():
#     directory = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0'
#     output_dir = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0\Parsed_Data'
#     # Iterate over each file in the directory
#     for filename in os.listdir(directory):
#         if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith('.jsonl'):
#             parse_game(os.path.join(directory, filename), os.path.join(directory, filename.split('.')[0] + '.json'), output_dir)


def parse_all_games():
    directory = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0' # change this path
    output_dir = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0\Parsed_Data'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each file in the directory
    for filename in os.listdir(directory):
        print(filename)
        file_path = os.path.join(directory, filename)
        if os.path.isfile(os.path.join(directory, filename)) and filename.lower().endswith('.jsonl'):
            json_filename = filename.rsplit('.', 1)[0] + '.json'
            output_file_path = os.path.join(output_dir, json_filename)

            # Check if the corresponding JSON file already exists in the Parsed_Data directory
            if not os.path.exists(output_file_path) and os.path.getsize(file_path) > 0:
                a = os.path.join(directory, filename)
                parse_game(a, json_filename, output_dir)


parse_all_games()
