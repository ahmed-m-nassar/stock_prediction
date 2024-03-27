"""
feature_engineering_pipeline.py

This script defines a feature engineering pipeline using scikit-learn's Pipeline and custom feature extractor transformers. The pipeline extracts various technical analysis features such as RSI, ADL, OBV, and MACD from input data.

Usage:
    python feature_engineering.py --output_artifact <output_data_name> --output_type <output_data_type>
                                           --output_description <output_data_description>

Arguments:
    --output_artifact (str): Name of the artifact for the extracted data to be saved in Weights & Biases (wandb).
    --output_type (str): Type of the output data artifact.
    --output_description (str): Description of the output data artifact.

Execution:
    - The script should be executed with required command-line arguments.
    - It initializes a wandb run to log the pipeline.
    - Constructs a feature engineering pipeline using scikit-learn's Pipeline and custom transformers.
    - Saves the constructed pipeline using MLflow.
    - Uploads the saved pipeline to Weights & Biases (wandb) with specified artifact name, type, and description.

"""

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

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(file_name='feature_engineering.log' ,level=logging.INFO, format=log_fmt)
class RSIFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to extract the Relative Strength Index (RSI) feature from input DataFrame.

    Attributes:
        None

    Methods:
        fit(self, X, y=None): Fit method required for scikit-learn transformers.
        transform(self, X): Transform method to extract RSI feature from input DataFrame.

    """

    def fit(self, X, y=None):
        """
        Fit method required for scikit-learn transformers.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.
            y (array-like): Target values (unused).

        Returns:
            self: Returns the instance itself.

        """
        return self

    def transform(self, X):
        """
        Transform method to extract RSI feature from input DataFrame.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.

        Returns:
            pandas.DataFrame: DataFrame containing the RSI feature.

        """
        df = X.copy()
        # Get RSI feature
        df['rsi_14'] = ta.rsi(df['close'], length=14)
        return df[['rsi_14']]


class ADLFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to extract the Accumulation Distribution Line (ADL) feature from input DataFrame.

    Attributes:
        None

    Methods:
        fit(self, X, y=None): Fit method required for scikit-learn transformers.
        transform(self, X): Transform method to extract ADL feature from input DataFrame.

    """

    def fit(self, X, y=None):
        """
        Fit method required for scikit-learn transformers.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.
            y (array-like): Target values (unused).

        Returns:
            self: Returns the instance itself.

        """
        return self

    def transform(self, X):
        """
        Transform method to extract ADL feature from input DataFrame.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.

        Returns:
            pandas.DataFrame: DataFrame containing the ADL feature.

        """
        df = X.copy()
        # Get ADL feature
        df['adl'] = (((df['close'] - df['close'].shift()) / (df['high'] - df['low'])) * df['volume']).fillna(0).cumsum()
        return df[['adl']]


class OBVFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to extract the On-Balance Volume (OBV) feature from input DataFrame.

    Attributes:
        None

    Methods:
        fit(self, X, y=None): Fit method required for scikit-learn transformers.
        transform(self, X): Transform method to extract OBV feature from input DataFrame.

    """

    def fit(self, X, y=None):
        """
        Fit method required for scikit-learn transformers.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.
            y (array-like): Target values (unused).

        Returns:
            self: Returns the instance itself.

        """
        return self

    def transform(self, X):
        """
        Transform method to extract OBV feature from input DataFrame.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.

        Returns:
            pandas.DataFrame: DataFrame containing the OBV feature.

        """
        df = X.copy()
        # Get OBV feature
        df['obv'] = (df['close'].diff() > 0).astype(int) * df['volume'].diff().fillna(0).cumsum()
        return df[['obv']]


class MACDFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer to extract the Moving Average Convergence Divergence (MACD) features from input DataFrame.

    Attributes:
        None

    Methods:
        fit(self, X, y=None): Fit method required for scikit-learn transformers.
        transform(self, X): Transform method to extract MACD features from input DataFrame.

    """

    def fit(self, X, y=None):
        """
        Fit method required for scikit-learn transformers.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.
            y (array-like): Target values (unused).

        Returns:
            self: Returns the instance itself.

        """
        return self

    def transform(self, X):
        """
        Transform method to extract MACD features from input DataFrame.

        Parameters:
            X (pandas.DataFrame): Input DataFrame containing the data.

        Returns:
            pandas.DataFrame: DataFrame containing the MACD features.

        """
        df = X.copy()
        # Get MACD features
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
    
if __name__ == '__main__':
    

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
    
