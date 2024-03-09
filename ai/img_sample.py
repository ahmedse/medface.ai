# ai/img_sample.py
from PIL import Image
import pandas as pd
import cv2
import os
import numpy as np

class ImgSample:
    def __init__(self, img_path, min_width=600, min_height=600):
        self.img_path = img_path
        self.min_width = min_width
        self.min_height = min_height
        self.validate_and_convert_image()
        self.image = Image.open(self.img_path)

    def validate_and_convert_image(self):
        try:
            img = Image.open(self.img_path)
        except IOError:
            raise Exception("Invalid image file")

        if img.size[0] < self.min_width or img.size[1] < self.min_height:
            raise Exception("Image size is less than the minimum required size")

        if img.format != 'JPEG':
            new_img_path = self.img_path.rsplit('.', 1)[0] + '.jpg'
            img.save(new_img_path, 'JPEG')
            os.remove(self.img_path)
            self.img_path = new_img_path

    def get_orientation(self):
        if self.image.size[0] > self.image.size[1]:
            return 'landscape'
        elif self.image.size[0] < self.image.size[1]:
            return 'portrait'
        else:
            return 'square'

    def detect_faces(self):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        img_cv2 = cv2.imread(self.img_path)
        gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        df_faces = pd.DataFrame([(x, y, w, h) for (x, y, w, h) in faces], columns=['x', 'y', 'width', 'height'])
        return df_faces