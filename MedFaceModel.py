import keras
from keras.preprocessing.image  import ImageDataGenerator
from keras_vggface.utils import preprocess_input
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import json
from keras_vggface.vggface import VGGFace
from keras.layers import GlobalAveragePooling2D, Flatten, Dense, Dropout
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import os
import logging

class MedFaceModel:
    def __init__(self, model_type, model_version, train_dir, val_dir, img_width, img_height, batch_size, epochs):
        self.model_type = model_type
        self.model_version = model_version
        self.train_dir = train_dir
        self.val_dir = val_dir
        self.img_width = img_width
        self.img_height = img_height
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = None
        self.train_generator = None
        self.val_generator = None
        self.checkpoint_filepath = f"models/model-{self.model_type}-{self.model_version}.h5"

    def setup_data_generators(self):
        """
        Set up the data generators for training and validation.
        """
        if not os.path.exists(self.train_dir) or not os.path.exists(self.val_dir):
            raise ValueError("One or both of the provided directories do not exist.")
        
        train_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            shear_range=0.2,
            zoom_range=0.2
            , brightness_range=(0.80, 1.0)
            , fill_mode='nearest'
            , rotation_range=10
            , horizontal_flip=True)
        
        val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
        
        self.train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            shuffle=True,
            color_mode='rgb',
            class_mode='categorical')
        
        self.val_generator = val_datagen.flow_from_directory(
            self.val_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical')
        
    def create_model(self):
        """
        Create a model based on VGGFace with custom top layers.
        """
        base_model = VGGFace(include_top=False,
                             model=self.model_type,
                             input_shape=(self.img_height, self.img_width, 3))

        for layer in base_model.layers:
            layer.trainable = False

        print(len(base_model.layers))

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Flatten()(base_model.output)
        x = Dense(2096, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(512, activation='relu')(x)
        preds = Dense(self.train_generator.num_classes, activation='softmax')(x)

        self.model = Model(inputs=base_model.input, outputs=preds)

        print(len(self.model.layers))

        self.model.compile(optimizer=Adam(lr=0.0001),
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    def train_model(self):
        """
        Train the model using the training and validation generators.
        """
        # check if model is created
        if self.model is None:
            print("Model is not defined. Please create a model before training.")
            return

        # check if generators are created
        if self.train_generator is None or self.val_generator is None:
            print("Data generators are not defined. Please setup data generators before training.")
            return

        # Ensure the models directory exists
        if not os.path.exists('models/'):
            os.makedirs('models/')

        # define the checkpoint
        checkpoint = ModelCheckpoint(self.checkpoint_filepath, monitor='val_loss', verbose=1,
                                    save_best_only=True, mode='min')
        callbacks_list = [checkpoint]
        # define early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=10)

        callbacks_list.append(early_stopping)

        # fit the model
        self.model.fit(
            self.train_generator,
            steps_per_epoch=self.train_generator.samples // self.batch_size,
            epochs=self.epochs,
            validation_data=self.val_generator,
            validation_steps=self.val_generator.samples // self.batch_size,
            callbacks=callbacks_list
            )

    def load_weights(self):
        """
        Load the model weights from the checkpoint file.
        """
        if not os.path.exists(self.checkpoint_filepath):
            raise ValueError("The checkpoint file does not exist.")
        if self.model is None:
            print("Model is not defined. Please create a model before loading weights.")
            return

        self.model.load_weights(self.checkpoint_filepath)

    def make_predictions(self):
        """
        Make predictions using the model.
        """
        if self.model is None:
            print("Model is not defined. Please create a model before making predictions.")
            return

        if self.val_generator is None:
            print("Validation generator is not defined. Please setup a validation generator before making predictions.")
            return

        predictions = self.model.predict(self.val_generator, steps=self.val_generator.samples // self.batch_size)
        return np.argmax(predictions, axis=1)
    
    def evaluate_model(self):
        """
        Evaluate the model on the validation set.
        """
        if self.model is None:
            print("Model is not defined. Please create a model before evaluating.")
            return

        if self.val_generator is None:
            print("Validation generator is not defined. Please setup a validation generator before evaluating.")
            return

        loss, acc = self.model.evaluate(self.val_generator, steps=self.val_generator.samples // self.batch_size)
        print(f'Validation loss: {loss}')
        print(f'Validation accuracy: {acc}')

    def compute_metrics(self):
        """
        Compute the classification metrics.
        """
        if self.val_generator is None:
            print("Validation generator is not defined. Please setup a validation generator before computing metrics.")
            return

        # Get the true labels
        true_labels = self.val_generator.classes

        # Make predictions
        predicted_labels = self.make_predictions()

        # Compute metrics
        report = classification_report(true_labels, predicted_labels, target_names=self.val_generator.class_indices.keys())
        confusion_matrix_values = confusion_matrix(true_labels, predicted_labels)

        return report, confusion_matrix_values

    def save_model(self):
        """
        Save the model to a file.
        """
        if self.model is None:
            print("Model is not defined. Please create a model before saving.")
            return

        self.model.save(self.checkpoint_filepath)

    def save_labels(self):
        """
        Save the labels to a file.
        """
        if self.train_generator is None:
            print("Training generator is not defined. Please setup a training generator before saving labels.")
            return

        labels = self.train_generator.class_indices
        with open('labels.json', 'w') as label_file:
            json.dump(labels, label_file)