# Read the file from datastream
import os
import sys
import pandas as pd
from src.logger import logging
from dataclasses import dataclass
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainer, ModelTrainerConfig

# Data Ingestion is the process of collecting, importing, and storing raw data from various sources into a system where it can be processed and analyzed. 
# Data ingestion involves:
# Reading the dataset (CSV file containing student performance data)
# Splitting it into training and testing sets for model development
# Saving the processed files in designated paths

# Decorator to simplify class creation by automatically generating common methods like __init__()
@dataclass                   
class DataIngestionConfig:
    # Train/Test/Raw data will be stored in this path
    raw_data_path: str = os.path.join('artifacts', 'data.csv')
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')    


class DataIngestion:
    """Class responsible for handling data ingestion"""
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """Read the dataset, performs train-test split, and save the file to disk"""
        logging.info("Entered in the data ingestion method or component")
        try:
            df = pd.read_csv(r"notebook\data\StudentsPerformance.csv")
            logging.info('Read the dataset as dataframe')

            # Create data path and make directory
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)   # Saved train file
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)     # Saved test file

            logging.info('Data Ingestion has been completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path)
        except Exception as e:
            logging.error(f"Exception occurred during data ingestion: {e}")
            raise CustomException("Failed to ingest data", str(e))

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    # Perform the data transformation
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)
    # Train the model
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))

