"""
save_prediction.py

This script saves prediction with model version with date into a database.

Usage:
    python predict.py --input_data_artifact <input_data_name> --used_model_artifact <used_model_name>
                                --database_url <database_url> --table_name <table_name>

Arguments:
    --input_data_artifact (str): Name of the input data artifact in Weights & Biases (wandb).
    --used_model_artifact (str): Name of the model artifact used for prediction in wandb.
    --database_url (str): URL of the database where prediction results will be stored.
    --table_name (str): Name of the table in the database where prediction results will be saved.


Execution:
    - The script should be executed with required command-line arguments.
    - It initializes a wandb run to log the prediction process.
    - Downloads the input data artifact from wandb.
    - Retrieves the trained model artifact used for prediction from wandb.
    - Prepares the prediction data by selecting necessary columns and adding model information.
    - Inserts the prediction data into the specified database table.
"""


import sys
import os
import logging
import argparse
import wandb
import pandas as pd

from sklearn.metrics import accuracy_score

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb
from src.utils.db_utils import connect_to_database , insert_df , close_connection

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_data_artifact", type=str, help="input data name in wandb", required=True)
    parser.add_argument("--used_model_artifact", type=str, help="model used in prediction", required=True)
    parser.add_argument("--database_url", type=str, help="database url", required=True)
    parser.add_argument("--table_name", type=str, help="table name to save the data", required=True)
    return parser.parse_args()
    
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='save_prediction.log', level=logging.INFO, format=log_fmt)

    logging.info("Starting prediction ...")
    args = parse_arguments()
    run = wandb.init()

    logging.info("Downloading data...")
    download_data_path = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts", "prediction")
    df = read_data_from_wandb(run, args.input_data_artifact, download_data_path)
    logging.info("Data downloaded successfully.")

    logging.info("Getting model version...")
    model_artifact = run.use_artifact(args.used_model_artifact)
    model_version = (model_artifact.name).split(':')[0] + ':' + model_artifact.version
    logging.info("Model version retrieved successfully.")

    logging.info("Preparing data...")
    df = df.iloc[[0]]
    df = df[['date', 'prediction']]
    df['feedback'] = None
    df['model_used'] = model_version
    logging.info("Data prepared successfully.")
    
    print(df.head())  # Print the prepared data

    logging.info("Inserting prediction into database...")
    connection = connect_to_database(args.database_url)
    insert_df(connection, df, table=args.table_name)
    close_connection(connection)
    logging.info("Prediction inserted into the database successfully.")

    wandb.finish()
