import os
from pathlib import Path
from src.datascienceproject import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from src.datascienceproject.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    ## Note: You can add different data transformation techniques such as Scaler, PCA and all
    #You can perform all kinds of EDA in ML cycle here before passing this data to the model

    # I am only adding train_test_spliting cz this data is already cleaned up
    def split_data(self):
        # Read data with semicolon separator
        data = pd.read_csv(self.config.data_path, sep=';')

        # Split the data
        train, test = train_test_split(data, test_size=0.2, random_state=42)
        
        # Save with semicolon separator to maintain consistency
        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), sep=';', index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), sep=';', index=False)

        logger.info("Columns in training data: %s", train.columns.tolist())

        logger.info("Split data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)

