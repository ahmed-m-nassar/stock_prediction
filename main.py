"""
MLflow Project Executor Script

This script executes an MLflow project with multiple
steps defined in the configuration.

It reads project configuration using Hydra
and sets up Weights & Biases (W&B) experiment.

The active steps are determined based on the configuration,
and each step is executedusing MLflow's `run` method with
specified parameters.

Usage:
    Run this script directly to execute the MLflow project.

Example:
    python executor.py

"""
import os
import mlflow
import hydra
from omegaconf import DictConfig
import json
import uuid


_steps = [
#    "data_ingestion",
#    "data_cleaning",
#     "data_seggregation",
    # "feature_engineering",
#    "training",
   "prediction"
     
]


# This automatically reads in the configuration
@hydra.main(version_base= None , config_path='.' , config_name='config')
def go(config: DictConfig):
    """
    Main function to execute the MLflow project.

    Args:
        config (DictConfig): Hydra configuration object
        containing project configuration.

    Returns:
        None
    """
    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    if "data_ingestion" in active_steps:
        # Download file and load in W&B
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "data_ingestion"),
            "main",
            env_manager="local",
            parameters={
                "stock_name": config["data_ingestion"]["stock_name"],
                "start_date": config["data_ingestion"]["start_date"],
                "end_date": config["data_ingestion"]["end_date"],
                "output_artifact": config["data_ingestion"]["stock_name"],
                "output_type": "raw_data",
                "output_description": "Stock raw data"
            },
        )
        
    if "data_cleaning" in active_steps:
        # Download file and load in W&B
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "data_cleaning"),
            "main",
            env_manager="local",
            parameters={
                "input_artifact": config["data_ingestion"]["stock_name"]+":latest",
                "output_artifact": "cleaned_data",
                "output_type": "cleaned_data",
                "output_description": "Stock data cleaned"
            },
        )
        
    if "data_seggregation" in active_steps:
        # Download file and load in W&B
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "data_seggregation"),
            "main",
            env_manager="local",
            parameters={
                "input_artifact": "cleaned_data:latest",
                "train_val_pct": config["data_segregation"]["train_val_pct"],
                "train_val_output_artifact": "train_val",
                "train_val_output_type": "train_val",
                "train_val_output_description": "train_val data for training and validation",
                "test_output_artifact": "test",
                "test_output_type": "test",
                "test_output_description": "test data"
            },
        )
        
    if "feature_engineering" in active_steps:
        # Extracts features for the model
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "feature_engineering"),
            "main",
            env_manager="local",
            parameters={
                "output_artifact": "feature_engineering_pipeline",
                "output_type": "pipeline",
                "output_description": "pipeline for feature engineering"
            },
        )
        
    if "training" in active_steps:
        # NOTE: we need to serialize the random forest configuration into JSON
        unique_id = uuid.uuid4()
        unique_filename = f"config_{unique_id}.json"
        xgboost_config = os.path.abspath(unique_filename)
        with open(xgboost_config, "w+") as fp:
            json.dump(dict(config["training"]["xgboost_classification"].items()), fp)  
        # NOTE: use the xgboost_config we just created as the xgboost_config parameter for the training
        # Extracts features for the model
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "training"),
            "main",
            env_manager="local",
            parameters={
                "input_data_artifact": "train_val:latest",
                "input_feature_engineering_artifact": "feature_engineering_pipeline:latest",
                "train_pct": config["training"]["train_size"],
                "xgboost_config": xgboost_config,
                "output_artifact": "trained_model",
                "output_type": "trained_model",
                "output_description": "model" 
            },
        )
        
    if "prediction" in active_steps:
        # Extracts features for the model
        _ = mlflow.run(
            os.path.join(hydra.utils.get_original_cwd(),
                         "src",
                         "prediction"),
            "main",
            env_manager="local",
            parameters={
                "input_data_artifact": "test:latest",
                "input_pipeline_artifact": "trained_model:production",
                "output_artifact": "prediction",
                "output_type": "preds",
                "output_description": "data predictions" 
            },
        )

if __name__ == "__main__":
    go()
