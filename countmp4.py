import json

# Load the JSON data
json_file_path = r"D:\University_Studies\Project\basalt-2022-behavioural-cloning-baseline\utils\all_10xx_Jun_29.json" # Replace with the path to your JSON file

with open(json_file_path, 'r') as file:
    data = json.load(file)

# Assuming the 'relpaths' list contains the paths to the mp4 files
mp4_files = [path for path in data['relpaths'] if path.endswith('.mp4')]

# Count the number of mp4 files
mp4_file_count = len(mp4_files)

print(f"There are {mp4_file_count} mp4 files listed in the file.")
