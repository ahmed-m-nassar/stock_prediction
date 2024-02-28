import pytest
from io import StringIO
import sys
import os
import types
from datetime import datetime
from unittest.mock import patch
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)
from src.data_ingestion.data_ingestion import get_stock_data_and_upload_to_wandb


@pytest.fixture
def mock_args():
    return types.SimpleNamespace(**{
    'stock_name': 'AAPL',
    'start_date': '2023-01-01',
    'end_date': '2023-01-10',
    'output_artifact': 'stock_data',
    'output_type': 'cleaned_data',
    'output_description': 'Data with outliers and null values removed'
})


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', end='2023-01-10'),
        'Open': [100.0] * 10,
        'High': [105.0] * 10,
        'Low': [95.0] * 10,
        'Close': [102.0] * 10,
        'Volume': [1000000] * 10,
        'Adj Close': [101.0] * 10
    })


@patch('src.data_ingestion.data_ingestion.yf.download')
@patch('src.data_ingestion.data_ingestion.wandb.init')
@patch('src.data_ingestion.data_ingestion.wandb.save')
@patch('src.data_ingestion.data_ingestion.wandb.finish')
def test_get_stock_data_and_upload_to_wandb(mock_finish, mock_save, mock_init, mock_download, mock_args, sample_data):
    os.environ["WANDB_PROJECT"] = "stock_predictor"
    os.environ["WANDB_RUN_GROUP"] = "test"
    # Setting up the mock for yfinance.download
    mock_download.return_value = sample_data

    # Calling the function under test
    get_stock_data_and_upload_to_wandb(mock_args)

    
    # Asserting calls to wandb functions
    mock_init.assert_called_once_with(name=mock_args.output_artifact, notes=mock_args.output_description)
    mock_save.assert_called_once_with(mock_args.output_artifact + '.csv')
    mock_finish.assert_called_once()

    # Asserting call to yfinance.download with correct arguments
    mock_download.assert_called_once_with(mock_args.stock_name, start=mock_args.start_date,
                                          end=mock_args.end_date)
