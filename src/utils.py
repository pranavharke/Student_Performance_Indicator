import os
import sys
import numpy as np
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException

# IT provides all the common utility functions for model saving, loading, and evaluating the model
    
def save_object(file_path, obj):
    # Saving model using Pickle
    # Pickle --> Used for serializing (saving) and deserializing (loading) objects into byte stream
    # A byte stream is a sequence of bytes used to represent data in binary format
    try:
        dir_path = os.path.dirname(file_path)
        # Create directory if does not exists
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)          # Saving file object as Pickle

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """Evaluates multiple machine learning models using GridSearchCV for hyperparameter tuning"""
    try:
        report = {}         # Empty dictionary to store the report paramters

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = param[list(models.keys())[i]]
            # Performing Hyper-parameter tuning using GridSearchCV
            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)
            # Set best parameters to the model and training it
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            # Computing R^2 score for model evaluation
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            # Store the test model in report dictionary
            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """Loads previously saved (i.e. trained model) from file object"""
    try:
        with open(file_path, "rb") as file_obj:
            # Loading file object using dill
            # dill --> It is an extension of pickle that provides more flexibility in serializing Python objects,
            # including custom functions, lambdas, and entire modules which is limited by pickle
            return dill.load(file_obj)        

    except Exception as e:
        raise CustomException(e, sys)