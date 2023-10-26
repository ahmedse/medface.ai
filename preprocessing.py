
import os
from PIL import Image  
import numpy as np

input_folder = 'output/acpc.teams/'
output_folder = 'output/headshots.by.person/'

for filename in os.listdir(input_folder):
    # Extract subfolder name from filename
    subfolder = filename.split('.')[0]
    #subfolder = name[:4]
    
    # Read image
    img = Image.open(os.path.join(input_folder, filename))
    
    # Resize image
    # resized = img.resize((224, 224))
    
    # Create subfolder if doesn't exist
    if not os.path.exists(os.path.join(output_folder, subfolder)):
        os.mkdir(os.path.join(output_folder, subfolder))
        
    # Save image to subfolder  
    img.save(os.path.join(output_folder, subfolder, filename))
    print(f'Saved {filename} to {subfolder} subfolder')