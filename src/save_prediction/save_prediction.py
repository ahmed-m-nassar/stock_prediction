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
    
    #Getting model version
    model_artifact = run.use_artifact(args.used_model_artifact)
    model_version = (model_artifact.name).split(':')[0] + ':' + model_artifact.version

    #Preparing data 
    df = df.iloc[[0]]
    df = df[['date', 'prediction']]
    df['feedback'] = None
    df['model_used'] = model_version
    
    print(df.head())
    #Inserting prediction in database
        
    connection = connect_to_database(args.database_url)
    insert_df(connection , df , table=args.table_name)
    close_connection(connection)

    wandb.finish()
    
