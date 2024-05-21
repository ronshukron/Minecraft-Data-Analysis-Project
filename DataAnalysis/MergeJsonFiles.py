import json
import glob
import os
import re

def extract_date(filename):
    match = re.search(r'(\d{8}-\d{6})', filename)
    return match.group(0) if match else None

def read_jsonl(file_path):
    data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    print(f"Skipping corrupted line in file: {file_path}")
                    continue
    except Exception as e:
        print(f"Skipping corrupted file: {file_path}. Error: {e}")
        return []
    return data

def read_jsonl_line(line):
    return json.loads(line)

def write_jsonl_line(data, file):
    json_line = json.dumps(data)
    file.write(json_line + '\n')

def write_json(data_list, file_path):
    """
    Writes a list of JSON objects to a file in JSONL format.
    :param data_list: List of JSON objects
    :param file_path: Path to the output file
    """
    with open(file_path, 'w') as file:  # Use 'w' to write, overwriting existing content
        for data in data_list:
            write_jsonl_line(data, file)

def merge_runs(input_directory, output_directory):
    json_files = glob.glob(os.path.join(input_directory, '*.jsonl'))
    json_files.sort(key=lambda x: extract_date(x))

    start_of_run = None
    merged_data = []
    i = -1
    for json_file in json_files:
        i += 1
        data = read_jsonl(json_file)
        if not data:
            print(f"Skipping empty or corrupted file: {json_file}")
            continue
        # Assuming each file contains a list of JSON objects
        if len(data) > 0 and len(data[0]["inventory"]) == 0:  # Start of a new run
            if start_of_run is not None:
                output_path = os.path.join(output_directory, f"merged_run_{start_of_run}.jsonl")
                write_json(merged_data, output_path)
                merged_data = []
            start_of_run = extract_date(json_file)  # Use the date as the run identifier
            merged_data.extend(data)  # Use extend to add elements of the list, not the list itself
        else:
            merged_data.extend(data)

    # Don't forget to save the last run if there is one
    if start_of_run is not None and len(merged_data) > 0:
        output_path = os.path.join(output_directory, f"merged_run_{start_of_run}.jsonl")
        write_json(merged_data, output_path)


# Set your input and output directories here
input_directory = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0\Raw_Data'
output_directory = r'C:\Users\Shira\Data\MineRLBasaltFindCave-v0\Merged_Files'

merge_runs(input_directory, output_directory)
