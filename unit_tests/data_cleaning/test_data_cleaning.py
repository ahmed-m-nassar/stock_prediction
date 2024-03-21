import sys
import os
from unittest.mock import patch
import pytest
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)
from src.data_cleaning.data_cleaning import clean_data

@pytest.fixture
def sample_data():
    index = pd.date_range(start='2024-01-01', periods=5, freq='D')
    data = {
        'open': [None, None, 3.0, 4.0, 5.0],
        'high': [1.0, None, 3.0, 4.0, 5.0],
        'low': [1.0, None, None, 4.0, 5.0],
        'close': [1.0, 2.0, 3.0, None, 5.0],
        'adj_close': [1.0, 2.0, 3.0, 4.0, None],
        'volume': [1.0, None, None, None, 5.0]
    }
    df = pd.DataFrame(data, index=index)
    return df

@pytest.fixture
def sample_data_column_names():
    # Define sample data with different column names and only two rows
    return pd.DataFrame({
        'Open': [1.0, 2.0],
        'High': [1.0, None],
        'Low': [1.0, None],
        'Close': [1.0, 2.0],
        'Adj Close': [1.0, 2.0],
        'Volume': [None, None]
    })

def test_clean_data_column_names(sample_data_column_names):
    # Call the clean_data function
    cleaned_data = clean_data(sample_data_column_names)

    # Define the expected column names
    expected_columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']

    # Check if the column names match the expected column names
    assert cleaned_data.columns.tolist() == expected_columns
    
def test_clean_data(sample_data):
    # Ensure data cleaning is applied successfully
    index = pd.date_range(start='2024-01-01', periods=5, freq='D')
    expected_output = {
        'open': [3.0, 3.0, 3.0, 4.0, 5.0],
        'high': [1.0, 2.0, 3.0, 4.0, 5.0],
        'low': [1.0, 2.0, 3.0, 4.0, 5.0],
        'close': [1.0, 2.0, 3.0, 4.0, 5.0],
        'adj_close': [1.0, 2.0, 3.0, 4.0, 4.0],
        'volume': [1.0, 2.0, 3.0, 4.0, 5.0]
    }
    expected_output = pd.DataFrame(expected_output, index=index)
    cleaned_data = clean_data(sample_data)
    print(cleaned_data)
    pd.testing.assert_frame_equal(cleaned_data, expected_output)


