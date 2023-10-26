import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
# pip install opencv-python-headless
# pip install mtcnn
# pip show mtcnn
import warnings
warnings.filterwarnings('ignore')
# face detection with mtcnn on a photograph
from mtcnn.mtcnn import MTCNN
from matplotlib import pyplot
import numpy as np
import cv2
import lib as l
from PIL import Image 
from pillow_heif import register_heif_opener
register_heif_opener()
detector = MTCNN()

def is_heic_file(file_path):
    return file_path.lower().endswith('.heic')

# specify path to raw images
input_path = f'raw'
output_path = f'datasets/y3'

def save_faces(image_path, result_list, output_dir = 'faces'):
    image = l.correct_image_orientation(image_path)
    image_rgb = image.convert('RGB')
    pixels = np.asarray(image_rgb)
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    for i, result in enumerate(result_list):
        x1, y1, width, height = result['box']        
        # x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        # Check if the face size is at least (224, 224)
        if width < 224 or height < 224:
            continue
        face = pixels[y1:y2, x1:x2]
        landmarks = result['keypoints']
        # adjusted_landmarks = {k: (v[0]-x1, v[1]-y1) for k, v in landmarks.items()}
        # aligned_face = align_face(face, adjusted_landmarks)
        # Convert back to image
        face_image = Image.fromarray(face)        
        if face_image is not None:
            output_image_path = os.path.join(output_dir, f'{base_name}_{i+1}.jpg')
            face_image.save(output_image_path)
            print(f"Face saved: {output_image_path}")


# iterate over files in the directory
for student_name in os.listdir(input_path):
    student_folder = os.path.join(input_path, student_name)
    if not os.path.isdir(student_folder):
        continue    
    # Create an output directory for this student
    student_output_folder = os.path.join(output_path, student_name)
    
    if not os.path.exists(student_output_folder):
        os.makedirs(student_output_folder)
        print(f"Folder created {student_output_folder}.")
    else:
        # The folder already exists, so do nothing
        print(f"Output folder already exists: {student_output_folder}")
        continue
        
    # Loop over the images in this student's folder
    for image_name in os.listdir(student_folder):
        image_path = os.path.join(student_folder, image_name)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        # Skip if not a file
        if not os.path.isfile(image_path):
            continue        
        # image = Image.open(image_path)
        image= l.correct_image_orientation(image_path)
        image_rgb = image.convert('RGB')
        pixels = np.asarray(image_rgb)
        
        if is_heic_file(image_path):
            print("The image is in HEIC format.")
            # pixels = pixels.transpose((1, 0, 2))
        else:
            print("The image is in JPEG format.")
            # pixels = pixels.transpose((1, 0, 2))
    
        faces_list = detector.detect_faces(pixels)
        for i, result in enumerate(faces_list):
            x1, y1, width, height = result['box']
            landmarks = result['keypoints']
            # Deal with negative pixel index
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            # Check if the face size is at least (224, 224)
            if width < 224 or height < 224:
                continue
            # Extract the face
            face = pixels[y1:y2, x1:x2]
            # Adjust landmarks to be relative to the cropped face
            adjusted_landmarks = {k: (v[0]-x1, v[1]-y1) for k, v in landmarks.items()}
            # Align the face
            aligned_face = l.align_face(face, adjusted_landmarks)
            # Convert back to image
            face_image = Image.fromarray(aligned_face)            
            if face_image is not None:
                output_image_path = os.path.join(student_output_folder, f'{base_name}_{i+1}.jpg')
                face_image.save(output_image_path)
                print(f"Face saved: {output_image_path}")
        print(image_path)
        # l.draw_image_with_boxes(image_path, faces_list)
