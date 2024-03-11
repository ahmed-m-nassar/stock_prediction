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
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logging.info("Starting prediction ...")
    args = parse_arguments()
    run = wandb.init()
    
    #Downloading data
    download_data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "prediction")

    df = read_data_from_wandb(run , args.input_data_artifact , download_data_path)
    logging.info(df.head())
    
    #Downloading pipeline
    download_pipeline_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 "models" ,
                                                 "full_pipeline")
    if os.path.exists(download_pipeline_path):
            shutil.rmtree(download_pipeline_path)
    pipeline_export_path = run.use_artifact(args.input_pipeline_artifact).download(root=download_pipeline_path)
    pipeline = mlflow.sklearn.load_model(pipeline_export_path)

   
    #prediction
    y_pred = pipeline.predict(df)
    df['prediction'] = y_pred    
    logging.info(df.head())
    
    #Saving data
    data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "prediction",
                                                 "prediction.csv")
    df.to_csv(data_path)
    upload_data_to_wandb(run ,
                         data_path ,
                         args.output_artifact,
                         args.output_type,
                         args.output_description ,
                         )
    
    wandb.finish()
    
