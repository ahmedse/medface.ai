import os
import tensorflow as tf
import keras
print("TensorFlow version: ", tf.__version__)
print("Keras version: ", keras.__version__)
import warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # FATAL
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import argparse
import shutil
from pathlib import Path
from matplotlib import pyplot
from PIL import Image
import xlsxwriter
import tempfile
from keras_vggface.utils import preprocess_input
import pickle
# from mtcnn.mtcnn import MTCNN
import cv2
from mtcnn import MTCNN
import lib as l
from contextlib import contextmanager
from functools import wraps
import sys
import io

def capture_output(func):
    """Wrapper to capture print output."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            return func(*args, **kwargs)
        finally:
            sys.stdout = old_stdout
    return wrapper

class NotAnImageFileError(Exception):
    pass

out_path= None
faceDetector = None
personDetector= None
person_labels= None

confidence_threshold= 0.99
min_face_size= 100

def extractFaces(image_path: str)-> pd.DataFrame:
    """
    This function extracts faces from an image file and returns them in a DataFrame.
    
    Parameters:
    img_file (str): Path to the image file

    Returns:
    pd.DataFrame: DataFrame containing all faces found in the image, each face is resized to (224, 224)
    """    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image = l.correct_image_orientation(image_path)
    image_rgb = image.convert('RGB')
    pixels = np.asarray(image_rgb)
    w_detect_face = capture_output(faceDetector.detect_faces) 
    faces = w_detect_face(pixels)
    faces_list, boxes_list = [], []
    for i, result in enumerate(faces):
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
    print(f"[INFO] Count of detected faces in image {base_name}: {len(faces_list)}")
    res_df= pd.DataFrame({'Face': faces_list, 'Box': boxes_list})
    return res_df

def decode_predictions(predictions, person_labels):
    prediction_indices = np.argmax(predictions, axis=1)    
    # Map the prediction index to the corresponding student name
    student_names = [person_labels[index] for index in prediction_indices]    
    # Get the highest probability (confidence)
    confidences = np.max(predictions, axis=1)    
    return student_names, confidences

def detectPersons(res_df) -> pd.DataFrame:
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
    return res_df

@contextmanager
def temporary_image_file(pil_img):
    pil_img = pil_img.resize((150, 150))
    fd, path = tempfile.mkstemp(suffix=".png")
    pil_img.save(path, format='PNG')
    try:
        yield path
    finally:
        os.close(fd)

def saveToExcel(faces_df, img_file: str):
    image_name = os.path.basename(img_file)
    # Assuming df is your DataFrame and it has a column 'face' that consists of PIL Image objects
    df = faces_df.copy()
    out_file= f"{img_file}.xlsx"

    stats_df= faces_df[['Predicted_team', 'Confidence']].groupby(['Predicted_team']).count().sort_values(['Confidence']
                                                                                                     , ascending=False)
    stats_df.rename(columns={'Confidence': 'Faces count'}, inplace=True)

    # Print the top teams in a beautifully formatted way
    top_team = stats_df.first_valid_index()
    print(f"Top predicted team in {image_name}: {top_team}, Faces count: {stats_df.loc[top_team, 'Faces count']}")

    # If the Excel file already exists, delete it
    if os.path.exists(out_file):
        os.remove(out_file)

    # Create a writer object
    writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
    # Write dataframe to excel without 'face' column
    df.drop('face', axis=1).to_excel(writer, sheet_name='Persons', index=False)
    stats_df.to_excel(writer, sheet_name='Stats', index=True)
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Persons']
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
    for idx, pil_img in enumerate(df['face'], start=2):
        with temporary_image_file(pil_img) as temp_img_path:
            worksheet.insert_image(f'C{idx}', temp_img_path, {'x_scale': 1, 'y_scale': 1, 'object_position': 3})
    # Close the Pandas Excel writer and output the Excel file
    writer.close()
    return out_file

def saveToWord(res_list):

    return True

def process_image(in_path):    
    faces_df= extractFaces(in_path)
    # print(f"Processing file {in_path} to detect persons in it...")
    persons_df= detectPersons(faces_df)
    results_file= saveToExcel(persons_df, in_path)
    # print(f"Processing completed. Results saved in {results_file}\n")

def process_folder(in_path):    
    res_list= []
    for image_path in in_path.glob('*'):
        if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:            
            faces_df= extractFaces(image_path)            
            persons_df= detectPersons(faces_df)
            res_list.append([persons_df, in_path])
    results_file= saveToWord(res_list)    
    # print(f"Processing completed. Results saved in {results_file}\n")

def main():
    global out_path
    global faceDetector
    global personDetector
    global person_labels

    parser = argparse.ArgumentParser(description='MedFace: Face detection system')
    parser.add_argument('-i', '--in', required=True, help='Path to image file or folder')
    parser.add_argument('-o', '--out', help='Path to output file')
    parser.add_argument('-t', '--lecturer', help='Which lecturer')
    parser.add_argument('-c', '--course', help='Which course')
    parser.add_argument('-s', '--segmodel', help='Path to segmentation file')
    parser.add_argument('-m', '--model', help='Path to model file')
    parser.add_argument('-l', '--labels', help='Path to labels file')
    args = vars(parser.parse_args())

    in_path = Path(args['in'])
    out_path = Path(args['out'] if args['out'] else in_path.parent)
    lecturer = args['lecturer'] if args['lecturer'] else 'N/A'
    course = args['course'] if args['course'] else 'N/A'
    model_path = Path(args['model'] if args['model'] else f"models/vgg16_model.h5")
    labels_path = Path(args['labels'] if args['labels'] else f"models/face-labels.pickle")

    print(f"Loading AI Engine ...")
    faceDetector = MTCNN()
    personDetector= load_model(model_path)    
    
    with open(labels_path, 'rb') as f:
        person_labels = pickle.load(f)

    if in_path.is_file():
        print(f"Process image file ...")
        if in_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            process_image(in_path)
        else:
            raise NotAnImageFileError(f"The file {in_path} is not an image file.")
    elif in_path.is_dir():
        print(f"Process folder ...")
        process_folder(in_path)
    else:
        print(f'Invalid input path: {in_path}')

if __name__ == "__main__":
    main()