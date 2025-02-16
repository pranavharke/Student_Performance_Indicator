import os
import sys
import pandas as pd
import numpy as np
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# Data Transformation is the process of modifying, converting, or restructuring raw data into a format suitable for analysis and machine learning.

# Decorator to simplify class creation by automatically generating common methods like __init__()
@dataclass
class DataTransformationConfig:
    preprocesssor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    """Class responsible for data transformation"""
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """This function is responsible for data transformation such as featuring engineering, encoding and scaling to optimize training and predictions"""
        try:
            numerical_columns = ['writing score', 'reading score']
            categorical_columns = [
                'gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course'
            ]

            # Handling Missing Values and scaling
            num_pipeline = Pipeline(
                steps=[
                    # Imputing missing value with median
                    ('impute', SimpleImputer(strategy='median')),
                    # Standardizing numerical features
                    ('scaler', StandardScaler())
                ]
            )

            # Processing categorical features
            cat_pipeline = Pipeline(
                steps=[
                    # Imputing missing values with most_frequent values
                    ('impute', SimpleImputer(strategy='most_frequent')),
                    # Categorical to numerical conversion
                    ('one_hot_encoder', OneHotEncoder()),
                    # Standardizing categorical features
                    ('scaler', StandardScaler())
                ]
            )

            logging.info(f'Categorical Columns: {categorical_columns}')
            logging.info(f'Numerical Columns: {numerical_columns}')

             # Combine preprocessing steps for numerical and categorical features
            preprocessor = ColumnTransformer(
                transformers=[
                                ('num', StandardScaler(with_mean=False), numerical_columns),    # Scaling numerical columns
                                ('cat', OneHotEncoder(), categorical_columns)                   # Encoding categorical columns
                            ]
                        )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Load train/test dataset
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Reading of train and test data completed...")
            logging.info('Obtaining preprocessor object...')
            # Getting preprocessor object
            preprocessor_obj = self.get_data_transformer_object()
            target_column_name = 'math score'
            numerical_columns = ['writing score', 'reading score']

            # Creating train set
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Creating test set
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f'Applying preprocessing object on training dataframe and testing dataframe')
            # Applying transformations 
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
            # Concatenate transformed features with target variable
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info(f'Saved preprocessing object...')
            # Save the object
            save_object(
                file_path=self.data_transformation_config.preprocesssor_obj_file_path,
                obj=preprocessor_obj)

            return train_arr, test_arr, self.data_transformation_config.preprocesssor_obj_file_path

        except Exception as e:
            raise CustomException(e, sys)


