# set up evaluation matrics
import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from src.datascienceproject.entity.config_entity import ModelEvaluationConfig
# set up configuration manager
from src.datascienceproject.constant import *  # Import all constants
from src.datascienceproject.utils.common import save_json  
import os
#os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/akatoshleiwu/datascienceproject_fullflow.mlflow"
#os.environ["MLFLOW_TRACKING_USERNAME"] = 
#os.environ["MLFLOW_TRACKING_PASSWORD"] = 


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def _preprocess_data(self, file_path):
        # Read the raw data
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Get column names from first line, removing extra quotes
        headers = lines[0].strip().strip('"').split(';')
        headers = [h.strip('"') for h in headers]
        
        # Process data rows
        data_rows = []
        for line in lines[1:]:
            values = line.strip().split(';')
            data_rows.append(values)
            
        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        # Convert numeric columns to appropriate types
        for col in df.columns:
            if col != 'quality':  # All columns except quality should be float
                df[col] = pd.to_numeric(df[col], errors='coerce')
            else:
                df[col] = pd.to_numeric(df[col], errors='coerce', downcast='integer')
        
        print(f"Processed data columns: {df.columns.tolist()}")
        print(f"First few rows of processed data:\n{df.head()}")
        
        return df

    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    
    def log_into_mlflow(self):
        # Preprocess the test data
        test_data = self._preprocess_data(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.TARGET_COLUMN], axis=1)
        test_y = test_data[[self.config.TARGET_COLUMN]]


        # Set tracking URI but don't set registry URI for DagsHub
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        # Start an MLflow run
        with mlflow.start_run():
            # Make predictions
            predicted_qualities = model.predict(test_x)
            
            # Calculate metrics
            (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
            
            # Save metrics locally
            from anyio import Path as AnyioPath
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=AnyioPath(str(self.config.metrics_file_name)), data=scores)

            # Log parameters and metrics to MLflow
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mae", mae)

            # Log the model without registration
            try:
                # Log model artifacts
                mlflow.sklearn.log_model(
                    sk_model=model,
                    artifact_path="model",
                )
                print(f"Model logged successfully in run {mlflow.active_run().info.run_id}")
            except Exception as e:
                print(f"Warning: Error while logging model: {str(e)}")
                print("Continuing with metric logging...")
    
