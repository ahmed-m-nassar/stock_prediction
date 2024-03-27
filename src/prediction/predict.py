"""
predict.py

This script performs prediction using a pre-trained machine learning pipeline on input data and saves the predictions.

Usage:
    python predict.py --input_data_artifact <input_data_name> --input_pipeline_artifact <input_pipeline_name>
                                --output_artifact <output_data_name> --output_type <output_data_type>
                                --output_description <output_data_description>

Arguments:
    --input_data_artifact (str): Name of the input data artifact in Weights & Biases (wandb).
    --input_pipeline_artifact (str): Name of the input pipeline artifact containing the pre-trained ML pipeline.
    --output_artifact (str): Name of the artifact for the predicted data to be saved in wandb.
    --output_type (str): Type of the output data artifact.
    --output_description (str): Description of the output data artifact.

Execution:
    - The script should be executed with required command-line arguments.
    - It initializes a wandb run to log the predictions.
    - Downloads the input data artifact from wandb.
    - Downloads the pre-trained ML pipeline artifact from wandb.
    - Uses the pipeline to perform prediction on the input data.
    - Saves the predictions along with input data to an artifact and uploads it to wandb.
"""


import sys
import os
import logging
import argparse
import shutil
import wandb
import json 
import mlflow
import uuid
import pandas as pd

from sklearn.metrics import accuracy_score

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb,upload_data_to_wandb

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='predict.log', level=logging.INFO, format=log_fmt)

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_data_artifact", type=str, help="input data name in wandb", required=True)
    parser.add_argument("--input_pipeline_artifact", type=str, help="input full pipeline artifact", required=True)
    parser.add_argument("--output_artifact", type=str, help="Name of the artifact for the cleaned data", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output data artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description of the output data artifact", required=True)
    return parser.parse_args()
    
    
if __name__ == '__main__':
    

    logging.info("Starting prediction ...")
    args = parse_arguments()
    run = wandb.init()

    logging.info("Downloading input data...")
    download_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "prediction")
    df = read_data_from_wandb(run, args.input_data_artifact, download_data_path)
    logging.info("Input data downloaded successfully.")

    logging.info("Downloading ML pipeline...")
    download_pipeline_path = os.path.join(os.path.dirname(__file__), "..", "models", "full_pipeline")
    if os.path.exists(download_pipeline_path):
        shutil.rmtree(download_pipeline_path)
    model_artifact = run.use_artifact(args.input_pipeline_artifact)
    pipeline_export_path = model_artifact.download(root=download_pipeline_path)
    pipeline = mlflow.sklearn.load_model(pipeline_export_path)
    logging.info("ML pipeline downloaded and loaded successfully.")

    logging.info("Performing prediction...")
    y_pred = pipeline.predict(df)
    df['prediction'] = y_pred
    logging.info("Prediction completed.")

    logging.info("Saving predicted data...")
    data_path = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "prediction", "prediction.csv")
    df.to_csv(data_path)
    upload_data_to_wandb(run, data_path, args.output_artifact, args.output_type, args.output_description)
    logging.info("Predicted data saved and uploaded successfully.")

    wandb.finish()
    logging.info("Prediction script completed.")

