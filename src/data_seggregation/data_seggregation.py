"""
data_seggregation.py

This script segregates input data into training and testing datasets based on a specified percentage split. It then uploads the segregated data to Weights & Biases (wandb).

Usage:
    python data_seggregation.py --input_artifact <input_data_name> --train_val_pct <train_val_percentage>
                                --train_val_output_artifact <train_val_output_data_name>
                                --train_val_output_type <train_val_output_data_type>
                                --train_val_output_description <train_val_output_data_description>
                                --test_output_artifact <test_output_data_name>
                                --test_output_type <test_output_data_type>
                                --test_output_description <test_output_data_description>

Arguments:
    --input_artifact (str): Name of the input data artifact in Weights & Biases (wandb).
    --train_val_pct (float): Percentage of data to be used for training, with the remainder for testing.
    --train_val_output_artifact (str): Name of the artifact for the training and validation data output in wandb.
    --train_val_output_type (str): Type of output data for training and validation data.
    --train_val_output_description (str): Description of the output data for training and validation data.
    --test_output_artifact (str): Name of the artifact for the testing data output in wandb.
    --test_output_type (str): Type of output data for testing data.
    --test_output_description (str): Description of the output data for testing data.

    
Execution:
    - The script should be executed with required command-line arguments.
    - It reads data from the specified input artifact in wandb.
    - Segregates the data into training and testing datasets based on the specified percentage split.
    - Saves the segregated datasets into CSV files.
    - Uploads the segregated data to wandb with specified artifact names, types, and descriptions.

Execution command example :
python data_seggregation.py \
    --input_artifact "input_data" \
    --train_val_pct 0.8 \
    --train_val_output_artifact "train_val_data" \
    --train_val_output_type "csv" \
    --train_val_output_description "Training and validation data" \
    --test_output_artifact "test_data" \
    --test_output_type "csv" \
    --test_output_description "Testing data"

"""



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

    """
    Segregate data into training and testing datasets.

    Parameters:
        df (pandas.DataFrame): Input DataFrame containing the data.
        split_pct (float): Percentage of data to be used for training, with the remainder for testing.

    Returns:
        tuple: A tuple containing the training DataFrame and testing DataFrame.
    """
    try:
        # Calculate the number of rows for training
        num_train_rows = int(len(df) * split_pct)

        # Split the DataFrame into training and testing
        train_data = df.iloc[:num_train_rows]
        test_data = df.iloc[num_train_rows:]

        return train_data, test_data
    
    except Exception as e:
        # Log the exception
        logging.error(f"Error occurred during data segregation: {e}")
        raise ValueError(f"Failed to seggregate data")

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(file_name='data_seggregation.log' ,level=logging.INFO, format=log_fmt)

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
    
