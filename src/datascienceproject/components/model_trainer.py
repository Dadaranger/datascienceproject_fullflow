import pandas as pd
import os
from src.datascienceproject import logger
from sklearn.linear_model import ElasticNet
import joblib

from src.datascienceproject.entity.config_entity import ModelTrainerConfig

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def _preprocess_data(self, file_path):
        # Read the raw data
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Get column names from first line, removing extra quotes
        headers = lines[0].strip().strip('"').split(';')
        headers = [h.strip('"').strip() for h in headers]  # Strip both quotes and whitespace
        
        # Process data rows
        data_rows = []
        for line in lines[1:]:
            # Split by semicolon and clean each value
            values = [val.strip().strip('"').strip() for val in line.strip().split(';')]
            data_rows.append(values)
            
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Convert numeric columns to appropriate types
        for col in df.columns:
            if col != 'quality':  # All columns except quality should be float
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
        
        logger.info(f"Processed data columns: {df.columns.tolist()}")
        logger.info(f"First few rows of processed data:\n{df.head()}")
        
        return df

    def train(self):
        # Load and preprocess data
        train_data = self._preprocess_data(self.config.train_data_path)
        test_data = self._preprocess_data(self.config.test_data_path)
        
        print("Available columns in training data:")
        print(train_data.columns.tolist())
        print("\nTarget column we're looking for:", self.config.target_column)
        
        # Add separator for readability
        print("\nFirst few rows of training data:")
        print(train_data.head())
        
        train_X = train_data.drop(columns=[self.config.target_column], axis=1)
        test_X = test_data.drop(columns=[self.config.target_column], axis=1)
        train_y = train_data[self.config.target_column]
        test_y = test_data[self.config.target_column]

        lr = ElasticNet(alpha=self.config.alpha, l1_ratio=self.config.l1_ratio, random_state=42)
        lr.fit(train_X, train_y)

        joblib.dump(lr, os.path.join(self.config.root_dir, self.config.model_name))
        
        logger.info("Model training completed.")