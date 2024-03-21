import pytest
import pandas as pd
import os
import sys
import logging

import numpy as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)
from src.feature_engineering.feature_engineering import RSIFeatureExtractor, ADLFeatureExtractor, OBVFeatureExtractor, MACDFeatureExtractor
import pandas_ta as ta


@pytest.fixture
def sample_data():
    # Create a sample DataFrame for testing
    data = {
    'date': ['2021-01-01', '2021-01-02', '2021-01-03', '2021-01-04', '2021-01-05',
             '2021-01-06', '2021-01-07', '2021-01-08', '2021-01-09', '2021-01-10',
             '2021-01-11', '2021-01-12', '2021-01-13', '2021-01-14', '2021-01-15',
             '2021-01-16', '2021-01-17', '2021-01-18', '2021-01-19', '2021-01-20',
             '2021-01-21', '2021-01-22', '2021-01-23', '2021-01-24', '2021-01-25',
             '2021-01-26', '2021-01-27', '2021-01-28', '2021-01-29', '2021-01-30',
             '2021-01-31', '2021-02-01', '2021-02-02', '2021-02-03', '2021-02-04',
             '2021-02-05', '2021-02-06', '2021-02-07', '2021-02-08', '2021-02-09',
             '2021-02-10', '2021-02-11', '2021-02-12', '2021-02-13', '2021-02-14',
             '2021-02-15', '2021-02-16', '2021-02-17', '2021-02-18', '2021-02-19'],
    'close': [10, 12, 15, 11, 13, 14, 16, 18, 15, 11, 10, 12, 14, 13, 15, 16, 18, 20, 19,
              17, 15, 14, 13, 12, 11, 10, 12, 15, 14, 16, 18, 17, 15, 14, 13, 12, 11, 10,
              12, 15, 14, 16, 18, 17, 15, 14, 13, 12, 11, 10],
    'high': [11, 13, 16, 12, 14, 15, 17, 19, 16, 12, 11, 13, 15, 14, 16, 17, 19, 21, 20,
             18, 16, 15, 14, 13, 12, 11, 13, 16, 15, 17, 19, 18, 16, 15, 14, 13, 12, 11,
             13, 16, 15, 17, 19, 18, 16, 15, 14, 13, 12, 11],
    'low': [9, 10, 13, 10, 11, 12, 14, 16, 13, 9, 8, 10, 12, 11, 13, 14, 16, 18, 17, 15,
            13, 12, 11, 10, 9, 8, 10, 13, 12, 14, 16, 15, 13, 12, 11, 10, 9, 8, 10, 13,
            12, 14, 16, 15, 13, 12, 11, 10, 9, 8],
    'volume': [1000, 2000, 1500, 1800, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600,
               2800, 3000, 3200, 3400, 3600, 3800, 4000, 4200, 4400, 4600, 4800, 5000,
               5200, 5400, 5600, 5800, 6000, 6200, 6400, 6600, 6800, 7000, 7200, 7400,
               7600, 7800, 8000, 8200, 8400, 8600, 8800, 9000, 9200, 9400, 9600, 9800,
               10000, 10200]
}


    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])  # Convert 'date' column to datetime
    df.set_index('date', inplace=True)  # Set 'date' column as index
    return df

def test_rsi_feature_extractor(sample_data):
    rsi_extractor = RSIFeatureExtractor()
    transformed_data = rsi_extractor.transform(sample_data)
    
    print(transformed_data)
    # Check if the transformed data has the expected column 'rsi_14'
    assert 'rsi_14' in transformed_data.columns
    assert len(transformed_data) == len(sample_data)    

def test_adl_feature_extractor(sample_data):
    adl_extractor = ADLFeatureExtractor()
    transformed_data = adl_extractor.transform(sample_data)
    print(transformed_data)

    # Check if the transformed data has the expected column 'adl'
    assert 'adl' in transformed_data.columns
    assert len(transformed_data) == len(sample_data) 
    
def test_obv_feature_extractor(sample_data):
    obv_extractor = OBVFeatureExtractor()
    transformed_data = obv_extractor.transform(sample_data)
    print(transformed_data)
    
    # Check if the transformed data has the expected column 'obv'
    assert 'obv' in transformed_data.columns
    assert len(transformed_data) == len(sample_data) 

def test_macd_feature_extractor(sample_data):
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logging.info("Saving feature engineering pipeline ...")
    macd_extractor = MACDFeatureExtractor()
    transformed_data = macd_extractor.transform(sample_data)
    print(transformed_data)
    # Check if the transformed data has the expected columns 'macd', 'macd_hist', and 'macd_signal'
    assert 'macd' in transformed_data.columns
    assert 'macd_hist' in transformed_data.columns
    assert 'macd_signal' in transformed_data.columns
    
    assert len(transformed_data) == len(sample_data) 