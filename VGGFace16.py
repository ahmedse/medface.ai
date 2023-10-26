# https://www.codemag.com/Article/2205081/Implementing-Face-Recognition-Using-Deep-Learning-and-Support-Vector-Machines
# https://github.com/bariarviv/VGGFace2

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import keras
print("TensorFlow version: ", tf.__version__)
print("Keras version: ", keras.__version__)
import pandas as pd
import numpy as np
#import tensorflow.keras as keras
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Dense, GlobalAveragePooling2D, Flatten
from keras.preprocessing import image
from keras.applications.mobilenet     import preprocess_input
from keras.preprocessing.image   import ImageDataGenerator
from keras.models import Model
from keras.optimizers import Adam
import random
from keras.callbacks import EarlyStopping, ModelCheckpoint

# Validate the model
def load_image(img_path, show=False):
    img = image.load_img(img_path, target_size=(224, 224))
    img_tensor = image.img_to_array(img)  # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)  # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.  # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])
        plt.axis('off')
        plt.show()
    return img_tensor

src_dir = f'datasets/y3.splitted/'
train_dir = f'datasets/y3.splitted/train/'
val_dir = f'datasets/y3.splitted/test/'
img_width, img_height = 224, 224
batch_size = 48
epochs = 100

train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input
                                    # , rescale=1. / 255
                                    , rotation_range=10  # Random rotation between -20 and +20 degrees                                    
                                    , shear_range=0.1  # Shear transformation with a maximum shear angle of 20 degrees
                                    , zoom_range=0.1  # Random zoom in/out of the image by up to 20%
                                    , brightness_range=(0.9, 1.1)
                                    #, contrast_stretching=True
                                    #, width_shift_range=0.2  # Random horizontal shift of up to 20% of the image width
                                    #, height_shift_range=0.2  # Random vertical shift of up to 20% of the image height
                                    , horizontal_flip=True  # Randomly flip the image horizontally
                                    #, vertical_flip=True  # Randomly flip the image vertically
                                    #, preprocessing_function=add_noise
                                    )

train_generator =  train_datagen.flow_from_directory(train_dir
                                                     , target_size=(img_height, img_width)
                                                     , color_mode='rgb'
                                                     , batch_size=batch_size
                                                     , class_mode='categorical'
                                                     , shuffle=True
                                                    )

val_datagen = ImageDataGenerator(
    # rescale=1. / 255
    )
val_generator = val_datagen.flow_from_directory(val_dir,
                                                target_size=(img_height, img_width),
                                                batch_size=batch_size,
                                                class_mode='categorical')

train_generator.class_indices.values()

# dict_values([0, 1, 2])
NO_CLASSES = len(train_generator.class_indices.values())

from keras_vggface.vggface import VGGFace
# vgg16, resnet50, senet50
model_type='vgg16'
base_model = VGGFace(include_top=False,
    model= model_type,
    input_shape=(img_height, img_width, 3))

for layer in base_model.layers:
    layer.trainable = False
base_model.summary()

print(len(base_model.layers))

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Flatten()(base_model.output)
x = Dense(4096, activation='relu')(x)
x = Dense(2048, activation='relu')(x)
# x = Dense(1024, activation='relu')(x)
preds = Dense(NO_CLASSES, activation='softmax')(x)
model = Model(inputs = base_model.input, outputs = preds)
model.summary()
print(len(model.layers))
# opt = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(optimizer='Adam'  
    # , optimizer='Adam'
    , loss='categorical_crossentropy'
    , metrics=['accuracy'])

# from tensorflow.keras.models import load_model
# model = load_model(f"models/vgg16_model_2.h5")
print("[INFO] training head...")
model.fit(train_generator,
          steps_per_epoch=np.ceil(train_generator.samples / batch_size),
          epochs=epochs,
          validation_data=val_generator,
          validation_steps=np.ceil(val_generator.samples / batch_size)
          # , callbacks=[early_stopping]
          )

import shutil
from glob import glob
class_labels = train_generator.class_indices
class_labels = {v: k for k, v in class_labels.items()}
results= []
for class_dir in os.listdir(val_dir):
    class_dir_path = os.path.join(val_dir, class_dir)
    # Make sure it's a directory
    if os.path.isdir(class_dir_path):
        # Iterate over each image in the class directory
        for img_path in os.listdir(class_dir_path):
            img_path_full = os.path.join(class_dir_path, img_path)
            # Make sure it's a file
            if os.path.isfile(img_path_full):
                new_image = load_image(img_path_full)
                pred = model.predict(new_image)
                # Decode the prediction
                pred_label = np.argmax(pred, axis=1)
                pred_label = class_labels[pred_label[0]]
                # Display the image and its predicted label
                # print(f"Image: {img_path}")
                # print(f"True label: {class_dir}")
                # print(f"Predicted label: {pred_label}")
                # load_image(img_path_full, show=True)
                results.append([class_dir, pred_label])

from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Separate the tuples into two lists: `y_true` and `y_pred`
y_true, y_pred = zip(*results)
conf_matrix = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred)
print("\nClassification Report:")
print(report)
accuracy = accuracy_score(y_true, y_pred)
print("\nAccuracy: ", accuracy)


# Save the model
model.save(f"models/{model_type}_model_2.h5")
print('\nSaved model.')
import pickle
class_dictionary = train_generator.class_indices
class_dictionary = {value:key for key, value in class_dictionary.items()}
print(class_dictionary)
# save the class dictionary to pickle
face_label_filename = r"models/face-labels.pickle"
with open(face_label_filename, 'wb') as f: pickle.dump(class_dictionary, f)
print('\nSaved labels.')

export_path = r"models/my_model/2"
import time
tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)