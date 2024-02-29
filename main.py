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


_steps = [
    "data_ingestion",
 #   "data_cleaning",
]


# This automatically reads in the configuration
@hydra.main(config_name='config')
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
                "output_artifact": "stock_data",
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
                "input_artifact": "stock_data:latest",
                "output_artifact": "cleaned_data",
                "output_type": "cleaned_data",
                "output_description": "Stock data cleaned"
            },
        )


if __name__ == "__main__":
    go()
