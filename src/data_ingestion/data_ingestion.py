"""
Stock Data Retrieval Script

This script retrieves historical stock data for a specified stock using the yfinance library.

Usage:
python data_ingestion.py --stock_name <stock_name> --start_date <start_date> --end_date <end_date> --output_artifact <output_artifact> --output_type <output_type> --output_description <output_description>

Author:
Ahmed Nassar

Arguments:
- stock_name (str): The name or ticker symbol of the stock to retrieve data for.
- start_date (str): The start date for the historical data in the format YYYY-MM-DD.
- end_date (str): The end date for the historical data in the format YYYY-MM-DD.
- output_artifact (str): The name of the output data in Weights & Biases.
- output_type (str): The type of output data.
- output_description (str): Description of the output data.

Example:
$ python data_ingestion.py --stock_name AAPL --start_date 2022-01-01 --end_date 2022-12-31 --output_artifact clean_stock_data --output_type cleaned_data --output_description "Data with outliers and null values removed"

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

    try:
        # Retrieve stock data using yfinance
        stock_data = yf.download(stock_name, start=start_date, end=end_date)

        # Check if data is retrieved successfully
        if stock_data.empty:
            raise ValueError(f"No data available for the stock '{stock_name}'")

        # Save stock data
        stock_data.to_csv(output_path, index=True)

        logging.info(f"Stock data downloaded and saved to {output_path}")

    except Exception as e:
        logging.error(f"An error occurred while downloading stock data: {str(e)}")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(file_name='data_ingestion.log' ,level=logging.INFO, format=log_fmt)

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