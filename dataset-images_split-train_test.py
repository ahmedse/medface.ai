import os
import shutil
import numpy as np
from glob import glob

# The source directory where the class subfolders are located
src_folder = 'datasets/y3'
# The target directories for the train and test split
train_folder = 'datasets/y3.splitted/train'
test_folder = 'datasets/y3.splitted/test'

# Create target directories if not exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# list comprehinsion to get class names from sub folders
classes = [d for d in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, d))]

for cls in classes:
    os.makedirs(os.path.join(train_folder, cls), exist_ok=True)
    os.makedirs(os.path.join(test_folder, cls), exist_ok=True)

    img_list = os.listdir(os.path.join(src_folder, cls))

    # Randomly shuffle the list
    np.random.shuffle(img_list)
    # Split images into 80% train and 20% test
    split_idx = int(0.9 * len(img_list))
    train_imgs = img_list[:split_idx]
    test_imgs = img_list[split_idx:]

    # Copy images into the train and test folders
    for img in train_imgs:
        shutil.copy(os.path.join(src_folder, cls, img), os.path.join(train_folder, cls, img))

    for img in test_imgs:
        shutil.copy(os.path.join(src_folder, cls, img), os.path.join(test_folder, cls, img))
    print(f'{cls}.')

print('Dataset splitting complete.')