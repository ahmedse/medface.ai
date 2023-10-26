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
from keras_vggface.utils import preprocess_input, decode_predictions
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

def extractFaces(img_file: str)-> pd.DataFrame:
    """
    This function extracts faces from an image file and returns them in a DataFrame.
    
    Parameters:
    img_file (str): Path to the image file

    Returns:
    pd.DataFrame: DataFrame containing all faces found in the image, each face is resized to (224, 224)
    """    
    pixels = pyplot.imread(img_file)  

    w_detect_face = capture_output(faceDetector.detect_faces) 
    faces = w_detect_face(pixels)
    faces_list_processed = []
    for i, result in enumerate(faces):
        x1, y1, width, height = result['box']
        x2, y2 = x1 + width, y1 + height
        # Disregard small images, considering them as noise
        if width < 100 or height < 100:
            continue  
        face = pixels[y1:y2, x1:x2]
        # extra step to ensure mtcnn detected face is correct
        validate_face= w_detect_face(face)
        if len(validate_face) < 1 or len(validate_face) > 1:
            continue
        face = Image.fromarray(face)
        # face_resized = face.resize((224, 224))
        faces_list_processed.append(face)
    faces_df = pd.DataFrame({'face': faces_list_processed})
    return faces_df

def detectPersons(faces_df) -> pd.DataFrame:
    faces_df['Predicted_person']= None
    faces_df['Predicted_team']= None
    faces_df['Confidence']= None
    for i, r in faces_df.iterrows():
        image = np.array(r['face']).astype(np.float64)  # Convert the image to a NumPy array
        image = preprocess_input(image, version=2)  # Preprocess the image for VGGFace
        image = np.expand_dims(image, axis=0)  # Add an extra dimension for batch size
        preds = personDetector.predict(image)
        # Get the predicted class index
        class_index = np.argmax(preds)
        faces_df.loc[i, 'Predicted_person']= person_labels[class_index]        
        tmp= person_labels[class_index]
        faces_df.loc[i, 'Predicted_team'] = tmp.split('_')[0]
        faces_df.loc[i, 'Confidence']= preds[0, class_index]

    # Sort the DataFrame by the largest count of non-null values in Predicted_team
    counts = faces_df['Predicted_team'].value_counts()
    faces_df = faces_df[faces_df['Predicted_team'].isin(counts.index)].sort_values(by='Predicted_team'
                                                                                , key=lambda x: counts[x]
                                                                                , ascending=False)
    return faces_df

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

def process_image(in_path):    
    faces_df= extractFaces(in_path)
    # print(f"Processing file {in_path} to detect persons in it...")
    persons_df= detectPersons(faces_df)
    results_file= saveToExcel(persons_df, in_path)
    # print(f"Processing completed. Results saved in {results_file}\n")

def main():
    global out_path
    global faceDetector
    global personDetector
    global person_labels

    parser = argparse.ArgumentParser(description='Image processing tool')
    parser.add_argument('-i', '--in', required=True, help='Path to image file or folder')
    parser.add_argument('-o', '--out', help='Path to output file')
    parser.add_argument('-s', '--segmodel', help='Path to segmentation file')
    parser.add_argument('-m', '--model', help='Path to model file')
    parser.add_argument('-l', '--labels', help='Path to labels file')
    args = vars(parser.parse_args())

    in_path = Path(args['in'])
    out_path = Path(args['out'] if args['out'] else in_path.parent)
    model_path = Path(args['model'] if args['model'] else f"models/vgg16_model.h5")
    labels_path = Path(args['labels'] if args['labels'] else f"models/face-labels.pickle")

    print(f"AI Engine loading ...")
    faceDetector = MTCNN()
    personDetector= load_model(model_path)    
    
    with open(labels_path, 'rb') as f:
        person_labels = pickle.load(f)

    if in_path.is_file():
        print(f"Process image file ...")
        if in_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
            process_image(in_path)
        else:
            raise NotAnImageFileError(f"The file {image_path} is not an image file.")
    elif in_path.is_dir():
        print(f"Process folder ...")
        for image_path in in_path.glob('*'):
            if image_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']:
                process_image(image_path)
            # else:
            #     raise NotAnImageFileError(f"The file {image_path} is not an image file.")
    else:
        print(f'Invalid input path: {in_path}')

if __name__ == "__main__":
    main()