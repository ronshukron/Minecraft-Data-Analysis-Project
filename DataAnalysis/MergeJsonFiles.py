import json
import glob
import os
import re



# def append_to_jsonl(data, file_path):
#     with open(file_path, 'a') as file:  # 'a' mode for appending to the file
#         for item in data:
#             file.write(json.dumps(item) + '\n')



def extract_date(filename):
    match = re.search(r'(\d{8}-\d{6})', filename)
    return match.group(0) if match else None

def read_jsonl(file_path):
    with open(file_path, 'r') as file:
        return [json.loads(line) for line in file]

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
























# def read_jsonl(file_path):
#     data = []
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             data.append(json.loads(line))
#     return data

# def read_jsonl_line(line):
#     return json.loads(line)

# def write_jsonl_line(data, file):
#     json_line = json.dumps(data)
#     file.write(json_line + '\n')

# def merge_runs(input_directory, output_directory):
#     json_files = sorted(glob.glob(os.path.join(input_directory, '*.jsonl')))
    # current_output_file = None
    # for json_file in json_files:
    #     with open(json_file, 'r') as file:
    #         for line in file:
    #             data = read_jsonl_line(line)
    #             # Check if this is the start of a new run based on inventory
    #             if len(data["inventory"]) == 0 and current_output_file is None:
    #                 # Start of a new run, open a new output file
    #                 output_path = os.path.join(output_directory, f"merged_run_{os.path.basename(json_file)}")
    #                 current_output_file = open(output_path, 'w')
    #             elif len(data["inventory"]) == 0 and current_output_file is not None:
    #                 # New run, but we have an open file, close it and start a new one
    #                 current_output_file.close()
    #                 output_path = os.path.join(output_directory, f"merged_run_{os.path.basename(json_file)}")
    #                 current_output_file = open(output_path, 'w')
    #             # Write the current action to the current output file
    #             write_jsonl_line(data, current_output_file)
    # # Close the last output file if it's open
    # if current_output_file is not None:
    #     current_output_file.close()

# Set your input and output directories here
input_directory = r'D:\University_Studies\Project\Task_10_only_json_test_100'
output_directory = r'D:\University_Studies\Project\Task_10_only_json_test_100_merged'

merge_runs(input_directory, output_directory)
