import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import argparse
import numpy as np
from keras.models import load_model
from sklearn.metrics import accuracy_score
from MedFaceModel import MedFaceModel
import tensorflow as tf
from numba import cuda
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier

def blending(predictions, val_labels):
    # Concatenate predictions
    blended_preds = np.c_[predictions].T
    
    # Train meta-learner
    meta_learner = MLPClassifier(random_state=1, max_iter=300).fit(blended_preds, val_labels)
    
    return meta_learner.predict(blended_preds)

def stacking(predictions, val_labels):
    # Concatenate predictions
    stacked_preds = np.c_[predictions].T
    
    # Train meta-learner
    meta_learner = MLPClassifier(random_state=1, max_iter=300).fit(stacked_preds, val_labels)
    
    return meta_learner.predict(stacked_preds)

def boosting(predictions, train_labels):
    # Concatenate predictions
    boosted_preds = np.c_[predictions].T
    
    # Train meta-learner
    ada = AdaBoostClassifier(random_state=1).fit(boosted_preds, train_labels)
    
    return ada.predict(boosted_preds)

def bagging(train_data, train_labels, val_data):
    # Initialize bagging classifier
    bagging = BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=10, random_state=0)
    
    # Fit and make predictions
    bagging.fit(train_data, train_labels)
    
    return bagging.predict(val_data)

def majority_voting(predictions):
    """Majority voting ensemble"""
    # Stack predictions
    predictions = np.array(predictions)
    
    # Get majority vote for each sample
    ensemble_preds = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)
    
    return ensemble_preds

def weighted_voting(predictions, weights):
    """Weighted voting ensemble"""
    # Stack predictions
    predictions = np.array(predictions)
    
    # Apply weights to the predictions
    weighted_preds = np.average(predictions, axis=0, weights=weights)
    
    # Round off to nearest integer to get final class label
    ensemble_preds = np.round(weighted_preds).astype(int)
    
    return ensemble_preds

def average_probabilities(probabilities):
    """Average probabilities ensemble"""
    # Average the probabilities
    avg_probabilities = np.mean(probabilities, axis=0)
    
    # Get class with highest average probability
    ensemble_preds = np.argmax(avg_probabilities, axis=-1)
    
    return ensemble_preds

def evaluate_ensemble(predictions, val_labels, ensemble_func, **kwargs):
    """Evaluate an ensemble"""
    # Check if ensemble_func is one of the functions that don't require val_labels
    if ensemble_func in [majority_voting, weighted_voting, average_probabilities, boosting]:
        # Get ensemble predictions without val_labels
        ensemble_preds = ensemble_func(predictions, **kwargs)
    else:
        # Get ensemble predictions with val_labels
        ensemble_preds = ensemble_func(predictions, val_labels, **kwargs)
    
    # Calculate and return accuracy
    return accuracy_score(val_labels, ensemble_preds)

def main(args):
    # Create the models
    print("Creating models...")
    vgg16_model = MedFaceModel('vgg16', '1.0', args.train_dir, args.val_dir, args.img_width, args.img_height, args.batch_size, args.epochs)
    resnet50_model = MedFaceModel('resnet50', '1.0', args.train_dir, args.val_dir, args.img_width, args.img_height, args.batch_size, args.epochs)
    senet50_model = MedFaceModel('senet50', '1.0', args.train_dir, args.val_dir, args.img_width, args.img_height, args.batch_size, args.epochs)

    # Setup the data generators
    print("Setting up data generators...")
    vgg16_model.setup_data_generators()
    resnet50_model.setup_data_generators()
    senet50_model.setup_data_generators()

    # Create, train, and delete each model
    models = [resnet50_model, senet50_model, vgg16_model]
    # for model in models:
    #     print(f"Creating and training model: {model.model_type}")
    #     model.create_model()
    #     model.train_model()
    #     model.save_model()

    #     # Clear the session and delete the model
    #     tf.keras.backend.clear_session()
    #     del model

    # cuda.select_device(0)
    # cuda.close()

    print("Getting validation data and labels...")
    val_data = []
    val_labels = []
    for i in range(len(vgg16_model.val_generator)):
        data, labels = next(vgg16_model.val_generator)
        val_data.extend(data)
        val_labels.extend(np.argmax(labels, axis=-1))

    # Convert the lists to numpy arrays
    val_data = np.array(val_data)
    val_labels = np.array(val_labels)

    # Load the models
    print("Loading models...")
    vgg16 = load_model(vgg16_model.checkpoint_filepath)
    resnet50 = load_model(resnet50_model.checkpoint_filepath)
    senet50 = load_model(senet50_model.checkpoint_filepath)  

    # Make predictions with each model
    print("Making predictions with each model...")
    vgg16_preds = np.argmax(vgg16.predict(val_data), axis=-1)
    resnet50_preds = np.argmax(resnet50.predict(val_data), axis=-1)
    senet50_preds = np.argmax(senet50.predict(val_data), axis=-1)

    # Calculate and print accuracy for each model
    print("Calculating accuracy for each model...")
    vgg16_accuracy = accuracy_score(val_labels, vgg16_preds)
    resnet50_accuracy = accuracy_score(val_labels, resnet50_preds)
    senet50_accuracy = accuracy_score(val_labels, senet50_preds)
    print(f"VGG16 accuracy: {vgg16_accuracy}")
    print(f"ResNet50 accuracy: {resnet50_accuracy}")
    print(f"SENet50 accuracy: {senet50_accuracy}")

    # Majority vote ensemble
    predictions = [vgg16_preds, resnet50_preds, senet50_preds]
    weights = [0.2, 0.3, 0.5]  # example weights

    print("Majority voting ensemble accuracy:",
        evaluate_ensemble(predictions, val_labels, majority_voting))
        
    print("Weighted voting ensemble accuracy:",
        evaluate_ensemble(predictions, val_labels, weighted_voting, weights=weights))

    # Average probabilities ensemble
    probabilities = [vgg16.predict(val_data), resnet50.predict(val_data), senet50.predict(val_data)]
    print("Average probabilities ensemble accuracy:",
        evaluate_ensemble(probabilities, val_labels, average_probabilities))
    
    # # Blending ensemble
    # print("Blending ensemble accuracy:",
    #     evaluate_ensemble(predictions, val_labels, blending))

    # # Boosting ensemble
    # print("Boosting ensemble accuracy:",
    #     evaluate_ensemble(predictions, val_labels, boosting))

    # # Bagging ensemble
    # print("Bagging ensemble accuracy:",
    #     evaluate_ensemble(val_data, val_labels, bagging, val_data=val_data))

    # # Stacking ensemble
    # print("Stacking ensemble accuracy:",
    #     evaluate_ensemble(predictions, val_labels, stacking))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train a model using MedFaceModel')
    parser.add_argument('--train_dir', type=str, default='datasets/y3.splitted/train/', help='Directory with training data')
    parser.add_argument('--val_dir', type=str, default='datasets/y3.splitted/test/', help='Directory with validation data')
    parser.add_argument('--img_width', type=int, default=224, help='Image width')
    parser.add_argument('--img_height', type=int, default=224, help='Image height')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    args = parser.parse_args()

    print("Starting the training...")
    main(args)