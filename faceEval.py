import keras
import tensorflow as tf
print("Keras version:", keras.__version__)
print("TensorFlow version:", tf.__version__)
import warnings
warnings.filterwarnings('ignore')
import os
import pandas as pd
import numpy as np
#import tensorflow.keras as keras
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
import cv2
from mtcnn import MTCNN
import lib as l
from PIL import Image
from keras_vggface.utils import preprocess_input, decode_predictions
import pickle
from functools import wraps
import xlsxwriter
import tempfile


# vgg16, resnet50, senet50
model_type='vgg16'
model_version= 3

faceDetector = MTCNN()
w_detect_face = l.capture_output(faceDetector.detect_faces) 
# personDetector = load_model(f"models/vgg16_model.h5")
personDetector = load_model(f"models/{model_type}_model_3.h5")
pred_list= []
with open(f"models/face-labels.pickle", 'rb') as f:
    person_labels = pickle.load(f)

def saveto_excel(persons_df):
    stats_df= persons_df[['Student', 'Confidence']].groupby(['Student']).count().sort_values(['Confidence']
                                                                                                        , ascending=False)
    stats_df.rename(columns={'Confidence': 'Faces count'}, inplace=True)
    image_name = os.path.basename(image_path)


    # Assuming df is your DataFrame and it has a column 'face' that consists of PIL Image objects
    df = faces_df.copy()
    # Create a writer object
    writer = pd.ExcelWriter(f"{image_path}.xlsx", engine='xlsxwriter')
    # Write dataframe to excel without 'face' column
    df.drop('Face', axis=1).to_excel(writer, sheet_name='Sheet1', index=False)
    stats_df.to_excel(writer, sheet_name='Stats', index=True)
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    # Set width and format for each column
    # Define cell format for center alignment
    cell_format = workbook.add_format()
    cell_format.set_align('top')
    worksheet.set_column('A:A', 15, cell_format)
    worksheet.set_column('B:B', 15, cell_format)
    # Set height for each row (assuming approximately 133 points = 100 pixels)
    for i in range(1, len(df) + 2):
        worksheet.set_row(i, 150)
    # Freeze the top row
    worksheet.freeze_panes(1, 0)
    # Iterate through each image and add to worksheet
    # Define a context manager to handle temporary file creation and deletion
    from contextlib import contextmanager
    @contextmanager
    def temporary_image_file(pil_img):
        pil_img = pil_img.resize((150, 150))
        fd, path = tempfile.mkstemp(suffix=".png")
        pil_img.save(path, format='PNG')
        try:
            yield path
        finally:
            os.close(fd)
            #os.remove(path)

    # Iterate through each image and add to worksheet
    for idx, pil_img in enumerate(df['Face'], start=2):
        with temporary_image_file(pil_img) as temp_img_path:
            worksheet.insert_image(f'C{idx}', temp_img_path, {'x_scale': 1, 'y_scale': 1, 'object_position': 3})

    # Close the Pandas Excel writer and output the Excel file
    writer.close()

def extractFaces(image_path: str)-> pd.DataFrame:
    """
    This function extracts faces from an image file and returns them in a DataFrame.
    
    Parameters:
    img_file (str): Path to the image file

    Returns:
    pd.DataFrame: DataFrame containing all faces found in the image, each face is resized to (224, 224)
    """    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    print(f"[INFO] Detecting faces in image {base_name}...")
    image = l.correct_image_orientation(image_path)
    image_rgb = image.convert('RGB')
    pixels = np.asarray(image_rgb)
    mtcnn_results = w_detect_face(pixels)
    faces_list, boxes_list = [], []
    for i, result in enumerate(mtcnn_results):
        x1, y1, width, height = result['box']
        x2, y2 = x1 + width, y1 + height
        # Disregard small images, considering them as noise
        if width < min_face_size or height < min_face_size:
            continue  
        face = pixels[y1:y2, x1:x2]
        validate_face= w_detect_face(face)
        validate_face = [res for res in validate_face if res['confidence'] >= confidence_threshold]
        if len(validate_face) != 1:
            continue
        landmarks = result['keypoints']
        adjusted_landmarks = {k: (v[0]-x1, v[1]-y1) for k, v in landmarks.items()}
        # Align the face
        face = l.align_face(face, adjusted_landmarks)
        face = Image.fromarray(face)
        face = face.resize((224, 224))
        faces_list.append(face)
        boxes_list.append(result['box'])
    print(f"[INFO] Count of detected faces: {len(mtcnn_results)}")
    res_df= pd.DataFrame({'Face': faces_list, 'Box': boxes_list})
    return res_df, mtcnn_results

def decode_predictions(predictions, person_labels):
    prediction_indices = np.argmax(predictions, axis=1)    
    # Map the prediction index to the corresponding student name
    student_names = [person_labels[index] for index in prediction_indices]    
    # Get the highest probability (confidence)
    confidences = np.max(predictions, axis=1)    
    return student_names, confidences

def detectPersons(res_df) -> pd.DataFrame:
    print(f"[INFO] Try to recognize persons...")
    res_df['Student']= None
    res_df['Confidence']= None
    faces_array = np.array([np.array(face.resize((224, 224))) for face in res_df['Face']])
    faces_array = faces_array.astype('float32')
    faces_array = preprocess_input(faces_array, version=1)  # version 2 is used for RESNET50 architecture
    predictions = personDetector.predict(faces_array)
    # Decode the predictions
    student_names, confidences = decode_predictions(predictions, person_labels)
    # Add student names and confidence to the DataFrame
    res_df['Student'] = student_names
    res_df['Confidence'] = confidences
    res_df = res_df.sort_values(['Student', 'Confidence'], ascending=[True, False]).reset_index(drop=True)
    print(f"[INFO] Count of recognized persons: {len(res_df)}")
    return res_df

# image_path= r"datasets\y3.test\big hall\WhatsApp Image 2023-09-30 at 2.27.54 PM (2).jpeg"
image_path= r"datasets/y3.test/big hall/WhatsApp Image 2023-09-30 at 2.27.52 PM (2).jpeg"
confidence_threshold= 0.99
min_face_size= 80

faces_df, mtcnn_results= extractFaces(image_path)
persons_df= detectPersons(faces_df)
saveto_excel(persons_df)

image_path_boxes= image_path + '_boxes.jpg'
orig_image_boxes= l.draw_image_with_boxes2(image_path, mtcnn_results, color='red')
orig_image_boxes.save(image_path_boxes)
res= persons_df['Box'].apply(lambda x: {'box': x})
orig_image_boxes= l.draw_image_with_boxes2(image_path_boxes, res, color='green')
orig_image_boxes.save(image_path_boxes)