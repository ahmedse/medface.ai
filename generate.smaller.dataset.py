import os
import shutil
import random

# Define source directory and destination directory
target= 'test' # test
src_dir = f'datasets/y3.splitted/{target}/'
dst_dir = f'datasets/y3.splitted.mini/{target}/'
percent= 1.0

# Make sure destination directory exists, if not, create it
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

# Iterate over each person's subfolder in the source directory
for person in os.listdir(src_dir):
    person_src_dir = os.path.join(src_dir, person)
    person_dst_dir = os.path.join(dst_dir, person)

    # Make sure the person's subfolder in the destination directory exists
    if not os.path.exists(person_dst_dir):
        os.makedirs(person_dst_dir)

    # Get a list of all file names in the person's source directory
    if os.path.isdir(person_src_dir):
        files = os.listdir(person_src_dir)

        # Calculate 20% of file count
        smaller_size = int(len(files) * percent)

        # Randomly sample 20% of the files
        smaller_files = random.sample(files, smaller_size)

        # Copy the smaller dataset into the person's destination directory
        for file_name in smaller_files:
            shutil.copy(os.path.join(person_src_dir, file_name), person_dst_dir)

        print(f"Copied {smaller_size} files from {person_src_dir} to {person_dst_dir}")