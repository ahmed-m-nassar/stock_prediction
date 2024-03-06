import sys
import os
import logging
import yfinance as yf
import pandas as pd
import argparse
import wandb
import shutil
import mlflow
import pandas_ta as ta
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline, FeatureUnion

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb,upload_data_to_wandb


class RSIFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        # Get RSI feature
        df['rsi_14'] = ta.rsi(df['close'], length=14)
        return df[['rsi_14']]

class ADLFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        # Get adl features
        df['adl'] = (((df['close'] - df['close'].shift()) / (df['high'] - df['low'])) * df['volume']).fillna(0).cumsum()
        return df[['adl']]

class OBVFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        # Get OBV features
        df['obv'] = (df['close'].diff() > 0).astype(int) * df['volume'].diff().fillna(0).cumsum()
        return df[['obv']]

class MACDFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy()
        # Get MACD Features
        macd = ta.macd(df['close'])
        df['macd'] = macd.iloc[:, 0]
        df['macd_hist'] = macd.iloc[:, 1]
        df['macd_signal'] = macd.iloc[:, 2]
        return df[['macd', 'macd_hist', 'macd_signal']]

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--output_artifact", type=str, help="Name of the artifact for the extracted data", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output data artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description of the output data artifact", required=True)
    return parser.parse_args()




# def extract_features(df):
#     #Get RSI feature
#     df['rsi_14'] = ta.rsi(df['close'], length=14)

#     #Get adl features
#     df['adl'] = (((df['close'] - df['close'].shift()) / (df['high'] - df['low'])) * df['volume']).fillna(0).cumsum()

#     #Get OBV features
#     df['obv']  = (df['close'].diff() > 0).astype(int) * df['volume'].diff().fillna(0).cumsum()
    
#     #Get MACD Features
#     macd = ta.macd(df['close'])
#     df['macd'] = macd.iloc[:, 0]  
#     df['macd_hist'] = macd.iloc[:, 1]  
#     df['macd_signal'] = macd.iloc[:, 2]  

#     return df
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logging.info("Saving feature engineering pipeline ...")
    args = parse_arguments()

    run = wandb.init()
    
    #Creating pipeline
    feature_pipeline = Pipeline([
        ('feature_union', FeatureUnion([
            ('rsi', RSIFeatureExtractor()),
            ('adl', ADLFeatureExtractor()),
            ('obv', OBVFeatureExtractor()),
            ('macd', MACDFeatureExtractor())
        ]))
    ])
    
    #Saving pipeline
    pipeline_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 "models",
                                                 "feature_engineering_pipeline")

    if os.path.exists(pipeline_path):
        shutil.rmtree(pipeline_path)
    mlflow.sklearn.save_model(feature_pipeline,pipeline_path )

    #Uploading pipeline
    upload_data_to_wandb(run ,
                         pipeline_path ,
                         args.output_artifact,
                         args.output_type,
                         args.output_description ,
                         metadata=None , 
                         file_flag=False
                         )
    
    wandb.finish()
    logging.info("Feature engineering pipeline saved successfully.")
    
