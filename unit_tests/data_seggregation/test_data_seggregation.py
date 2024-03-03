import os
import sys
import pytest
import pandas as pd

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)
from src.data_seggregation.data_seggregation import segregate_data

@pytest.fixture
def test_data():
    # Sample test data
    return pd.DataFrame({'A': [1, 2, 3, 4], 'B': [6, 7, 8, 9]})

def test_segregate_data(test_data):
    # Test for split percentage of 0.5
    train_data, test_data = segregate_data(test_data, 0.5)
    assert len(train_data) == 2
    assert len(test_data) == 2
