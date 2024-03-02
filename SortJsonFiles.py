import json
from datetime import datetime

def sort_by_date(item):
    # Extracting date and time from the filename
    date_str = item.split('-')[-2]  # Assumes date and time are always in the same position
    time_str = item.split('-')[-1].split('.')[0]  # Remove file extension
    datetime_obj = datetime.strptime(date_str + time_str, '%Y%m%d%H%M%S')
    return datetime_obj

def sort_json_file(input_path, output_path):
    # Reading the JSON file
    with open(input_path, 'r') as file:
        data = json.load(file)

    # Sorting the 'relpaths' array by date and time
    sorted_relpaths = sorted(data['relpaths'], key=sort_by_date)

    # Updating the 'relpaths' array with the sorted list
    data['relpaths'] = sorted_relpaths

    # Writing the sorted data to a new JSON file
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=2)

# Replace these paths with your actual file paths
input_path = r"D:\University_Studies\Project\basalt-2022-behavioural-cloning-baseline\utils\all_10xx_Jun_29.json"
output_path = r"D:\University_Studies\Project\basalt-2022-behavioural-cloning-baseline\utils\Sorted_all_10xx_Jun_29.json"

sort_json_file(input_path, output_path)
