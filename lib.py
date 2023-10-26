# mtcnn

# pip install opencv-python-headless
# pip install mtcnn
# pip show mtcnn

import warnings
warnings.filterwarnings('ignore')
# face detection with mtcnn on a photograph
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
# from mtcnn.mtcnn import MTCNN
import cv2
from mtcnn import MTCNN
from PIL import Image, ImageDraw
import numpy as np
from contextlib import contextmanager
from functools import wraps
import sys
import io
from pillow_heif import register_heif_opener
register_heif_opener()

def convert_heic_to_jpg(directory):
    # Go through all files in the directory (including subdirectories)
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file is a HEIC file
            if file.endswith(".heic") or file.endswith(".HEIC"):
                heic_path = os.path.join(root, file)
                # Construct the output path
                jpg_path = os.path.splitext(heic_path)[0] + ".jpg"
                # Open the image using PIL, which can now handle HEIC files
                image = Image.open(heic_path)
                # Save the image in JPEG format
                image.save(jpg_path, format="JPEG")
                # Delete the original file
                os.remove(heic_path)
                print(f"Converted '{heic_path}' to '{jpg_path}' and deleted the original file.")

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

def correct_image_orientation(image_path, output_path=""):
    image = Image.open(image_path)
    # Check if the image has EXIF orientation information
    if hasattr(image, "_getexif") and image._getexif() is not None:
        exif = dict(image._getexif().items())
        # Get the orientation tag (key: 274)
        orientation = exif.get(274)
        # Rotate the image based on the orientation tag
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)    
    # Save the corrected image
    # image.save(output_path)
    return image


def draw_image_with_boxes2(image_path, result_list, color='red'):
    image = correct_image_orientation(image_path) 
    image_rgb = image.convert('RGB')
    draw = ImageDraw.Draw(image_rgb)
    margin= 5
    for result in result_list:
        x, y, width, height = result['box']
        x, y = abs(x), abs(y)
        rect = [x - margin, y - margin, x + width + margin, y + height + margin]
        draw.rectangle(rect, outline=color, width=3)
    image_rgb.show()
    return image_rgb

# draw an image with detected objects
def draw_image_with_boxes(image_path, result_list):
    image = correct_image_orientation(image_path)
    image_rgb = image.convert('RGB')
    pixels = np.asarray(image_rgb)
    pyplot.imshow(pixels)
    # get the context for drawing boxes
    ax = pyplot.gca()
    # plot each box
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        x, y = abs(x), abs(y)
        rect = Rectangle((x, y), width, height, fill=False, color='red')
        # draw the box
        ax.add_patch(rect)
    pyplot.axis('off')
    # show the plot
    pyplot.show()

# draw an image with detected objects
def draw_image_with_boxes_circles(filename, result_list):
    # load the image
    data = pyplot.imread(filename)
    # plot the image
    pyplot.imshow(data)
    # get the context for drawing boxes
    ax = pyplot.gca()
    # plot each box
    for result in result_list:
        # get coordinates
        x, y, width, height = result['box']
        # create the shape
        rect = Rectangle((x, y), width, height, fill=False, color='red')
        # draw the box
        ax.add_patch(rect)
        # draw the dots
        for key, value in result['keypoints'].items():
            # create and draw dot
            dot = Circle(value, radius=2, color='red')
            ax.add_patch(dot)
    pyplot.axis('off')
    # show the plot
    pyplot.show()

 # draw each face separately
def draw_faces(filename, result_list):
	# load the image
	data = pyplot.imread(filename)
	# plot each face as a subplot
	for i in range(len(result_list)):
		# get coordinates
		x1, y1, width, height = result_list[i]['box']
		x2, y2 = x1 + width, y1 + height
		# define subplot
		pyplot.subplot(1, len(result_list), i+1)
		pyplot.axis('off')
		# plot face
		pyplot.imshow(data[y1:y2, x1:x2])
	pyplot.show()
        
from matplotlib import pyplot
import os

def align_face(face, landmarks):
    # Calculate the angle between the two eyes
    dx = landmarks['right_eye'][0] - landmarks['left_eye'][0]
    dy = landmarks['right_eye'][1] - landmarks['left_eye'][1]
    angle = np.degrees(np.arctan2(dy, dx))
    # Get the center of the face
    center = (face.shape[1] / 2, face.shape[0] / 2)
    # Generate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # Perform the rotation
    aligned_face = cv2.warpAffine(face, M, (face.shape[1], face.shape[0]))
    return aligned_face

def save_faces(filename, result_list, output_dir = 'faces'):
    # load the image
    data = pyplot.imread(filename)
    # get the base name of the file (without extension)
    base_name = os.path.splitext(os.path.basename(filename))[0]
    # directory to save faces
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # iterate over faces
    for i, result in enumerate(result_list):
        # get coordinates
        x1, y1, width, height = result['box']
        x2, y2 = x1 + width, y1 + height
        # extract face
        face = data[y1:y2, x1:x2]
        # construct output file path
        output_file = os.path.join(output_dir, f'{base_name}_{i+1}.jpg')
        # save face
        pyplot.imsave(output_file, face)
        


def correct_image_orientation(image_path, output_path=""):
    image = Image.open(image_path)
    # Check if the image has EXIF orientation information
    if hasattr(image, "_getexif") and image._getexif() is not None:
        exif = dict(image._getexif().items())
        # Get the orientation tag (key: 274)
        orientation = exif.get(274)
        # Rotate the image based on the orientation tag
        if orientation == 3:
            image = image.rotate(180, expand=True)
        elif orientation == 6:
            image = image.rotate(270, expand=True)
        elif orientation == 8:
            image = image.rotate(90, expand=True)    
    # Save the corrected image
    # image.save(output_path)
    return image

def is_heic_file(file_path):
    return file_path.lower().endswith('.heic')

def align_face(face, landmarks):
    # Calculate the angle between the two eyes
    dx = landmarks['right_eye'][0] - landmarks['left_eye'][0]
    dy = landmarks['right_eye'][1] - landmarks['left_eye'][1]
    angle = np.degrees(np.arctan2(dy, dx))
    # Get the center of the face
    center = (face.shape[1] / 2, face.shape[0] / 2)
    # Generate the rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, 1)
    # Perform the rotation
    aligned_face = cv2.warpAffine(face, M, (face.shape[1], face.shape[0]))
    return aligned_face

def detect_faces(filename= 'test2.jpg'):
    # load image from file
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(pixels)
    # display faces on the original image
    #draw_faces(filename, faces)
    return faces