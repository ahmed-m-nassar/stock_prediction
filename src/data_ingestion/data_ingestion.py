"""
Stock Data Retrieval Script

This script retrieves historical stock data for a specified stock using the yfinance library.

Usage:
    python stock_data_retrieval.py

Author:
    [Your Name]

Requirements:
    - Python 3.x
    - yfinance library (install using `pip install yfinance`)

Example:
    $ python stock_data_retrieval.py

Notes:
    - This script requires an active internet connection to retrieve stock data from the Yahoo Finance API.
    - Ensure that the provided stock name is valid and exists on the Yahoo Finance platform.

"""
import logging
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
