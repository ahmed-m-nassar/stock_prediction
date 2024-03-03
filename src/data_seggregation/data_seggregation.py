

import sys
import os
import logging
import yfinance as yf
import argparse
import wandb


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

    parser.add_argument("--input_artifact", type=str, help="input data name in wandb", required=True)
    parser.add_argument("--train_val_pct", type=float, help="training and val data percentage", required=True)
    parser.add_argument("--train_val_output_artifact", type=str, help="output data name in wandb", required=True)
    parser.add_argument("--train_val_output_type", type=str, help="type of output data", required=True)
    parser.add_argument("--train_val_output_description", type=str, help="description of the output data", required=True)
    parser.add_argument("--test_output_artifact", type=str, help="output data name in wandb", required=True)
    parser.add_argument("--test_output_type", type=str, help="type of output data", required=True)
    parser.add_argument("--test_output_description", type=str, help="description of the output data", required=True)

    return parser.parse_args()

def segregate_data(df, split_pct):
    """
    Segregate data into training and testing datasets.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing the data.
        split_pct (float): Percentage of data to be used for training, with the remainder for testing.

    Returns:
        tuple: A tuple containing the training DataFrame and testing DataFrame.
    """
    # Calculate the number of rows for training
    num_train_rows = int(len(df) * split_pct)

    # Split the DataFrame into training and testing
    train_data = df.iloc[:num_train_rows]
    test_data = df.iloc[num_train_rows:]

    return train_data, test_data    

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logging.info("Starting data_seggregation ...")
    args = parse_arguments()
    
    run = wandb.init()
        
    download_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "data_cleaning")
    
    cleaned_data = read_data_from_wandb(run , args.input_artifact , download_path )
    
    train_val_data , test_data = segregate_data(cleaned_data , args.train_val_pct)
    
    train_val_data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "data_seggregation",
                                                 "train_val.csv")
    train_val_data.to_csv(train_val_data_path)
    
    test_data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "data_seggregation",
                                                 "test.csv")
    test_data.to_csv(test_data_path)
    
    upload_data_to_wandb(run ,
                         train_val_data_path ,
                         args.train_val_output_artifact,
                         args.train_val_output_type,
                         args.train_val_output_description)
    
    upload_data_to_wandb(run ,
                         test_data_path ,
                         args.test_output_artifact,
                         args.test_output_type,
                         args.test_output_description)

    wandb.finish()
    
