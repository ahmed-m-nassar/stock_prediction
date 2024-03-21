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
from src.data_ingestion.data_ingestion import  download_stock_data, parse_arguments


def test_download_stock_data():
    output_path = 'test_stock_data.csv'
    
    if os.path.exists(output_path):
        os.remove(output_path)
        
    download_stock_data('AAPL' , '2022-01-01', '2022-01-10', output_path)
    data = pd.read_csv(output_path)
    
    assert not data.empty
    assert os.path.exists(output_path)
    
    os.remove(output_path) 
       
