"""
training_script.py

This script performs training of an XGBoost classifier on preprocessed data and saves the trained model along with its configuration.

Usage:
    python train.py  --input_data_artifact <input_data_name> --input_feature_engineering_artifact <input_feature_engineering_pipeline>
                               --train_pct <train_data_percentage> --xgboost_config <xgboost_config_file>
                               --output_artifact <output_model_name> --output_type <output_model_type>
                               --output_description <output_model_description>

Arguments:
    --input_data_artifact (str): Name of the input data artifact in Weights & Biases (wandb).
    --input_feature_engineering_artifact (str): Name of the feature engineering pipeline artifact in wandb.
    --train_pct (float): Percentage of data to be used for training.
    --xgboost_config (str): Path to the XGBoost configuration file.
    --output_artifact (str): Name of the artifact for the trained model to be saved in wandb.
    --output_type (str): Type of the output model artifact.
    --output_description (str): Description of the output model artifact.

Execution:
    - The script should be executed with required command-line arguments.
    - It initializes a wandb run to log the training process.
    - Downloads the input data and feature engineering pipeline artifacts from wandb.
    - Splits the data into training and validation datasets.
    - Trains an XGBoost classifier on the training data.
    - Evaluates the trained model on the validation data and logs the accuracy.
    - Saves the trained model along with its configuration and uploads it to wandb.
"""


import sys
import os
import logging
import argparse
import shutil
import wandb
import json 
import xgboost as xgb
import mlflow
import uuid
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.metrics import accuracy_score

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb,upload_data_to_wandb

class TransformerWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, transformer):
        self.transformer = transformer
    
    def fit(self, X, y=None):
        return self.transformer.fit(X, y)
    
    def transform(self, X):
        return self.transformer.transform(X)
    
def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_data_artifact", type=str, help="input data name in wandb", required=True)
    parser.add_argument("--input_feature_engineering_artifact", type=str, help="input feature engineering pipeline in wandb", required=True)
    parser.add_argument("--train_pct", type=float, help="training data percentage", required=True)
    parser.add_argument("--xgboost_config", type=str)
    parser.add_argument("--output_artifact", type=str, help="Name of the artifact for the cleaned data", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output data artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description of the output data artifact", required=True)
    return parser.parse_args()

def split_data(df, pct):
    """
    Split the DataFrame into training and validation datasets.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing the data.
        pct (float): Percentage of data to be used for training.

    Returns:
        tuple: A tuple containing the training DataFrame and validation DataFrame.
    """
    try:
        # Calculate the number of rows for training
        num_train_rows = int(len(df) * pct)

        # Split the DataFrame into training and validation
        train_data = df.iloc[:num_train_rows].copy()
        val_data = df.iloc[num_train_rows:].copy()
        
        return train_data, val_data
    except Exception as e:
        logging.error(f"Error occurred while splitting data: {str(e)}")
        return None, None


def train_xgboost(df, target_name, xgboost_config):
    """
    Train an XGBoost classifier.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing the training data.
        target_name (str): Name of the target variable.
        xgboost_config (dict): Configuration parameters for the XGBoost classifier.

    Returns:
        xgb.XGBClassifier: Trained XGBoost classifier.
    """
    try:
        # Define the XGBoost classifier
        clf = xgb.XGBClassifier(**xgboost_config)

        # Train the classifier
        clf.fit(df.drop(columns=[target_name]), df[target_name])
        
        return clf
    except Exception as e:
        logging.error(f"Error occurred while training XGBoost classifier: {str(e)}")
        return None


def transform_data(df, pipeline):
    """
    Transform input data using a feature engineering pipeline.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing the data.
        pipeline (sklearn.pipeline.Pipeline): Feature engineering pipeline.

    Returns:
        pandas.DataFrame: Transformed DataFrame with features and labels.
    """
    try:
        # Create labels
        df["tomorrow"] = df["close"].shift(-1)
        df["label"] = (df["tomorrow"] > df["close"]).astype(int)
        df.reset_index(drop=True, inplace=True)

        # Transform data using the pipeline
        features_df = pipeline.transform(df)
        features_df = pd.DataFrame(features_df)
        features_df["label"] = df["label"].copy()
        features_df.dropna(inplace=True)

        return features_df
    except Exception as e:
        logging.error(f"Error occurred while transforming data: {str(e)}")
        return None

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='train.log', level=logging.INFO, format=log_fmt)

    try:
        logging.info("Starting training ...")
        args = parse_arguments()

        # Get the XGBoost configuration and update W&B
        with open(args.xgboost_config) as fp:
            xgboost_config = json.load(fp)

        run = wandb.init()

        # Downloading data
        download_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "feature_engineering")
        df = read_data_from_wandb(run, args.input_data_artifact, download_data_path)
        logging.info("Data downloaded successfully.")

        # Downloading feature engineering pipeline
        download_feature_engineering_path = os.path.join(os.path.dirname(__file__), "..", "models", "feature_engineering")
        if os.path.exists(download_feature_engineering_path):
            shutil.rmtree(download_feature_engineering_path)
        feature_engineering_export_path = run.use_artifact(args.input_feature_engineering_artifact).download(root=download_feature_engineering_path)
        feature_engineering = mlflow.sklearn.load_model(feature_engineering_export_path)
        logging.info("Feature engineering pipeline downloaded successfully.")

        # Splitting data
        train_df, val_df = split_data(df, args.train_pct)
        logging.info("Data split into train and validation sets.")

        # Training
        transformed_train_df = transform_data(train_df, feature_engineering)
        model = train_xgboost(transformed_train_df, 'label', xgboost_config)
        logging.info("Model trained successfully.")

        # Evaluation
        transformed_val_df = transform_data(val_df, feature_engineering)
        y_pred = model.predict(transformed_val_df.drop(columns=['label']))
        accuracy = accuracy_score(y_pred, transformed_val_df['label'])
        run.summary['accuracy'] = accuracy
        logging.info(f"Accuracy: {accuracy}")

        # Saving full pipeline
        full_pipeline = Pipeline([
            ('feature_engineering', TransformerWrapper(feature_engineering)),
            ('model', model)
        ])
        unique_id = uuid.uuid4()
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", f"config_{unique_id}")
        if os.path.exists(model_path):
            shutil.rmtree(model_path)
        mlflow.sklearn.save_model(full_pipeline, model_path)
        logging.info("Full pipeline saved successfully.")

        # Uploading pipeline to W&B
        upload_data_to_wandb(run, model_path, args.output_artifact, args.output_type, args.output_description,
                             metadata=xgboost_config, file_flag=False)
        logging.info("Pipeline uploaded to W&B.")

        shutil.rmtree(model_path)
        os.remove(args.xgboost_config)
        wandb.finish()
        logging.info("Training completed.")

    except Exception as e:
        logging.error(f"An error occurred during training: {str(e)}")
