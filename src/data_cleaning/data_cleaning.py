"""
Data Cleaning and Upload Script

This script reads ingested data from Weights & Biases, applies data cleaning steps,
and uploads the cleaned data back to Weights & Biases.

Usage:
    python data_cleaning.py --input_artifact <input_artifact> --output_artifact <output_artifact> --output_type <output_type> --output_description <output_description>

Author:
    Ahmed Nassar

Arguments:
    - input_artifact (str): The name of the artifact containing the ingested data.
    - output_artifact (str): The name of the artifact to be created for the cleaned data.
    - output_type (str): The type of the output data artifact.
    - output_description (str): Description of the output data artifact.

Example:
    $ python data_cleaning.py --input_artifact stock_data --output_artifact clean_stock_data --output_type cleaned_data --output_description "Data with interpolated missing values"

"""

import os
import sys
import argparse
import logging
import wandb
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb,upload_data_to_wandb

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='data_cleaning.log' ,level=logging.INFO, format=log_fmt)

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
    - argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Data Cleaning and Upload Script")
    parser.add_argument("--input_artifact", type=str, help="Name of the artifact containing the ingested data", required=True)
    parser.add_argument("--output_artifact", type=str, help="Name of the artifact for the cleaned data", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output data artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description of the output data artifact", required=True)
    return parser.parse_args()


def clean_data(df):
    """
    Apply data cleaning steps to the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    try:
        logging.info("Cleaning data...")
        #df.set_index('Date')
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        df['open'] = df['open'].interpolate(method='linear' , limit_direction = 'both')
        df['high'] = df['high'].interpolate(method='linear', limit_direction = 'both')
        df['low'] = df['low'].interpolate(method='linear', limit_direction = 'both')
        df['close'] = df['close'].interpolate(method='linear', limit_direction = 'both')
        df['adj_close'] = df['adj_close'].interpolate(method='linear', limit_direction = 'both')
        df['volume'] = df['volume'].interpolate(method='linear', limit_direction = 'both')
        logging.info("Data cleaned successfully")
        return df
    except Exception as e:
        logging.error(f"Error occurred while cleaning data: {str(e)}")
        raise ValueError(f"Failed to clean data: {str(e)}")

if __name__ == "__main__":
    try:
        
        run = wandb.init()
        
        # Parse command-line arguments
        args = parse_arguments()

        # Read data from W&B
        data = read_data_from_wandb(run ,
                                    args.input_artifact ,
                                    os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "data_ingestion"))
        data.set_index('Date')
        # Clean the data
        cleaned_data = clean_data(data)
        cleaned_data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "data_cleaning",
                                                 "cleaned_data.csv")
        cleaned_data.to_csv(cleaned_data_path)

        upload_data_to_wandb(run , cleaned_data_path , args.output_artifact, args.output_type, args.output_description)

        wandb.finish()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise ValueError(f"Script execution failed: {str(e)}")
