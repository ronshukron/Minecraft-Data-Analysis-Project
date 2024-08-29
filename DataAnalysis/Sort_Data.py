import os
import shutil
import random

# Path to the folder containing the JSON files
source_folder = r'C:\Data\House_Building_rng'
# Create the destination folders
percentages = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
destination_folders = [os.path.join(source_folder, str(p)) for p in percentages]

# Ensure all folders are created
for folder in destination_folders:
    os.makedirs(folder, exist_ok=True)

# List all JSON files in the source folder
all_files = [f for f in os.listdir(source_folder) if f.endswith('.json')]
random.shuffle(all_files)

# Calculate the number of files for each percentage
total_files = len(all_files)
files_per_folder = [(p, int(total_files * (p / 100))) for p in percentages]

# Copy files to the respective folders
for i, (percent, file_count) in enumerate(files_per_folder):
    for file in all_files[:file_count]:
        for folder in destination_folders[i:]:
            src = os.path.join(source_folder, file)
            dst = os.path.join(folder, file)
            shutil.copyfile(src, dst)

print("Files have been distributed successfully.")
