import os
import shutil
import numpy as np
import pandas as pd
from glob import glob
from PIL import Image
from pillow_heif import register_heif_opener
import lib as l
from mtcnn import MTCNN
detector = MTCNN()
register_heif_opener()

l.convert_heic_to_jpg(r'D:\\1- ws.projects\medface\webapp\media\y3.personal')

# The source directory where the class subfolders are located
src_folder = 'raw'
# The target directories for the train and test split
dest_folder = 'datasets/y3.personal'

# Create target directories if not exist
os.makedirs(dest_folder, exist_ok=True)

# list comprehinsion to get class names from sub folders
classes = [d for d in os.listdir(src_folder) if os.path.isdir(os.path.join(src_folder, d))]
split_list = [item.split('_') for item in classes]
df = pd.DataFrame(split_list, columns=['ID', 'Name'])
df['label']= classes
duplicates = df[df.duplicated('ID', keep=False)]
print(duplicates)
df = df.drop_duplicates(subset='ID')
df.to_csv('Y3_students.csv', index=False)

df= pd.read_csv('Y3_students.csv')
df_csv = pd.read_excel('Year3 2023-2024.xlsx')
merged_df = df.merge(df_csv, on='ID')

merged_df = pd.merge(df, df_csv, how='outer', indicator=True)
missing_rows = merged_df[merged_df['_merge'] == 'right_only']
missing_rows.to_excel('missing.xlsx', index=False)
merged_df.to_excel('merged_df.xlsx', index=False)

for cls in classes:   
    folder= os.path.join(dest_folder, cls) 
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        print(f"Folder created {folder}.")
    else:
        # The folder already exists, so do nothing
        print(f"Output folder already exists: {folder}")
        continue    

    img_list = os.listdir(os.path.join(src_folder, cls))
    src_path= os.path.join(src_folder, cls, img_list[0])
    
    # resize image
    img = l.correct_image_orientation(src_path) #Image.open(src_path)
    img = img.convert("RGB")
    img_array = np.array(img)
    
    faces = detector.detect_faces(img_array)
    if len(faces) > 0:
        x, y, w, h = faces[0]['box']
        face_center_x = x + w // 2
        face_center_y = y + h // 2
        bbox_half_width = w // 2
        bbox_half_height = h // 2
        crop_x = max(face_center_x - bbox_half_width, 0)
        crop_y = max(face_center_y - bbox_half_height, 0)
        crop_width = min(w, img.width - crop_x)
        crop_height = min(h, img.height - crop_y)
        
        crop_x -= 350
        crop_y -= 250
        crop_width += 800
        crop_height += 1200
        crop_x = max(crop_x, 0)
        crop_y = max(crop_y, 0)
        crop_width = min(crop_width, img.width - crop_x)
        crop_height = min(crop_height, img.height - crop_y)
        cropped_image = img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))
        # cropped_image = img.crop((crop_x + margin, crop_y + margin, crop_x + crop_width + margin, crop_y + crop_height+ margin))

        # Resize the cropped image to a width of 400 pixels while maintaining the aspect ratio
        target_width = 400
        target_height = int(target_width * cropped_image.height / cropped_image.width)
        resized_image = cropped_image.resize((target_width, target_height))
     
        dest_path = os.path.join(dest_folder, cls, img_list[0].lower().replace(os.path.splitext(img_list[0])[1], '.jpg'))      
        resized_image.save(dest_path)
            
    # shutil.copy(os.path.join(src_folder, cls, img_list[0]), os.path.join(dest_folder, cls, img_list[0]))

print('Dataset splitting complete.')