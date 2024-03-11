import sys
import os
import logging
import argparse
import shutil
import wandb
import json 
import xgboost as xgb
import mlflow
import uuid
import pandas as pd

from sklearn.metrics import accuracy_score

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, parent_dir)

from src.utils.utils import read_data_from_wandb,upload_data_to_wandb

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_data_artifact", type=str, help="input data name in wandb", required=True)
    parser.add_argument("--input_feature_engineering_artifact", type=str, help="input feature engineering pipeline in wandb", required=True)
    parser.add_argument("--train_pct", type=float, help="training data percentage", required=True)
    parser.add_argument("--xgboost_config", type=str)
    parser.add_argument("--output_artifact", type=str, help="Name of the artifact for the cleaned data", required=True)
    parser.add_argument("--output_type", type=str, help="Type of the output data artifact", required=True)
    parser.add_argument("--output_description", type=str, help="Description of the output data artifact", required=True)
    return parser.parse_args()

def split_data(df , pct) :
    # Calculate the number of rows for training
    num_train_rows = int(len(df) * pct)

    # Split the DataFrame into training and testing
    train_data = df.iloc[:num_train_rows].copy()
    val_data = df.iloc[num_train_rows:].copy()
    return train_data , val_data

def train_xgboost(df , target_name , xgboost_config) :
    # Define the XGBoost classifier
    clf = xgb.XGBClassifier(
        **xgboost_config
    )

    # Train the classifier
    clf.fit(df.drop(columns = [target_name]), df[target_name])
    return clf

def transform_data(df , pipeline):
    #Create labels
    df["tomorrow"] = df["close"].shift(-1)
    df["label"] = (df["tomorrow"] > df["close"]).astype(int)
    df.reset_index(drop=True, inplace=True)
    
    features_df = pipeline.transform(df)
    features_df = pd.DataFrame(features_df)
    features_df["label"] = df["label"].copy()
    features_df.dropna(inplace=True)

    return features_df
    
    
if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    logging.info("Starting training ...")
    args = parse_arguments()
    # Get the Random Forest configuration and update W&B
    with open(args.xgboost_config) as fp:
        xgboost_config = json.load(fp)
    
    run = wandb.init()
    
    #Downloading data
    download_data_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 ".." ,
                                                 "artifacts" ,
                                                 "feature_engineering")

    df = read_data_from_wandb(run , args.input_data_artifact , download_data_path )
    
    #Downloading pipeline
    download_pipeline_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 "models" ,
                                                 "feature_engineering")

    if os.path.exists(download_pipeline_path):
        shutil.rmtree(download_pipeline_path)
        
    pipeline_export_path = run.use_artifact(args.input_feature_engineering_artifact).download(root=download_pipeline_path)
    pipeline = mlflow.sklearn.load_model(pipeline_export_path)

    #Splitting data
    train_df , val_df = split_data(df , args.train_pct)

    #Training
    transformed_train_df = transform_data(train_df , pipeline)
    model = train_xgboost(transformed_train_df, 'label' ,xgboost_config)
    
    #Evaluation
    transformed_val_df = transform_data(val_df , pipeline)
    y_pred = model.predict(transformed_val_df.drop(columns = ['label']))
    accuracy = accuracy_score(y_pred, transformed_val_df['label'])
    run.summary['accuracy'] = accuracy
    print("Accuracy:", accuracy)
    
    #Saving model
    unique_id = uuid.uuid4()
    model_path = os.path.join(os.path.dirname(__file__),
                                                 "..",
                                                 "models",
                                                 f"config_{unique_id}")
    if os.path.exists(model_path):
        shutil.rmtree(model_path)
    mlflow.sklearn.save_model(model,model_path )

    upload_data_to_wandb(run ,
                         model_path ,
                         args.output_artifact,
                         args.output_type,
                         args.output_description ,
                         metadata=xgboost_config , 
                         file_flag=False
                         )
    
    shutil.rmtree(model_path)
    os.remove(args.xgboost_config)
    wandb.finish()
    
