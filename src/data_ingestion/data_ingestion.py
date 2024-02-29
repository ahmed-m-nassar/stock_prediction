"""
Stock Data Retrieval Script

This script retrieves historical stock
data for a specified stock using the yfinance library.

Usage:
    python data_ingestion.py --stock_name <stock_name> --output_artifact <output_artifact> --output_type <output_type> --output_description <output_description>

Author:
    Ahmed Nassar

Arguments:
    - stock_name (str): The name or ticker symbol of the stock to retrieve data for.
    - output_artifact (str): The name of the output data in Weights & Biases.
    - output_type (str): The type of output data.
    - output_description (str): Description of the output data.

Example:
    $ python stock_data_retrieval.py --stock_name AAPL --output_artifact clean_stock_data --output_type cleaned_data --output_description "Data with outliers and null values removed"

Notes:
    - This script requires an active internet connection to retrieve stock data from the Yahoo Finance API.
    - Ensure that the provided stock name is valid and exists on the Yahoo Finance platform.

"""

import sys
import os
import logging
import yfinance as yf
import argparse
import wandb


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import upload_data_to_wandb

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock_name", type=str, help="stock name to download its data", required=True)
    parser.add_argument("--start_date", type=str, help="start date of historical data of stock", required=True)
    parser.add_argument("--end_date", type=str, help="end date of historical data of stock", required=True)
    parser.add_argument("--output_artifact", type=str, help="output data name in wandb", required=True)
    parser.add_argument("--output_type", type=str, help="type of output data", required=True)
    parser.add_argument("--output_description", type=str, help="data cleaning is applied to the input data", required=True)
    return parser.parse_args()

def download_stock_data(stock_name, start_date, end_date, output_path):
    """
    Download stock data from Yahoo Finance and save it to a CSV file.

    Parameters:
        stock_name (str): The name of the stock.
        start_date (str): The start date for the historical data (YYYY-MM-DD).
        end_date (str): The end date for the historical data (YYYY-MM-DD).
        output_path (str): The path where the downloaded data will be saved.

    Raises:
        ValueError: If no data is available for the specified stock.

    Returns:
        None
    """
    logging.info(f"Downloading data for {stock_name} stock")
    
    # Retrieve stock data using yfinance
    stock_data = yf.download(stock_name, start=start_date, end=end_date)
    
    # Check if data is retrieved successfully
    if stock_data.empty:
        raise ValueError(f"No data available for the stock '{stock_name}'")
    
    # Save stock data
    stock_data.to_csv(output_path, index=True)

    logging.info(f"Stock data downloaded and saved to {output_path}")

def get_stock_data_and_upload_to_wandb(args):
    """
    Retrieve historical stock data for the specified stock name and upload it to Weights & Biases.

    Parameters:
    - args (argparse.Namespace): An object containing the parsed command-line arguments.
      It should have the following attributes:
        - stock_name (str): The name or ticker symbol of the stock to retrieve data for.
        - output_artifact (str): The name of the output data in Weights & Biases.
        - output_type (str): The type of output data.
        - output_description (str): Description of the output data.
    """
    try:

        # Upload data to Weights & Biases
        logging.info("Uploading " + args.stock_name + " stock to wandb")

        wandb.init()

        artifact = wandb.Artifact(
                args.output_artifact,
                type=args.output_type,
                description=args.output_description,
                )

        artifact.add_file(f"{args.output_artifact}.csv")
        run.log_artifact(artifact)
        wandb.finish()

        print("""Stock data saved and uploaded
              to Weights & Biases successfully!""")
    except Exception as e:
        # Log and raise an error if data retrieval or upload fails
        raise ValueError(f"""Failed to retrieve or upload
                         data for the stock '{args.stock_name}': {str(e)}""")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logging.info("Starting data_ingestion ...")
    args = parse_arguments()
    
    download_path = os.path.join(os.path.dirname(__file__),
                                     "..",
                                     ".." ,
                                     "artifacts" ,
                                     "data_ingestion",
                                     args.stock_name + '.csv')
    download_stock_data(args.stock_name,
                        args.start_date,
                        args.end_date,
                        download_path)
        
    run = wandb.init()
    upload_data_to_wandb(run ,download_path, args.output_artifact, args.output_type, args.output_description )
    wandb.finish()