import json
import mlflow
import tempfile
import os
import wandb
import hydra
from omegaconf import DictConfig

_steps = [
    "data_ingestion",
  
    # NOTE: We do not include this in the steps so it is not run by mistake.
    # You first need to promote a model export to "prod" before you can run this,
    # then you need to run this step explicitly
#    "test_regression_model"
]


# This automatically reads in the configuration
@hydra.main(config_name='config')
def go(config: DictConfig):
    
    # Setup the wandb experiment. All runs will be grouped under this name
    os.environ["WANDB_PROJECT"] = config["main"]["project_name"]
    os.environ["WANDB_RUN_GROUP"] = config["main"]["experiment_name"]

    # Steps to execute
    steps_par = config['main']['steps']
    active_steps = steps_par.split(",") if steps_par != "all" else _steps

    # Move to a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:

        if "data_ingestion" in active_steps:
            # Download file and load in W&B
            _ = mlflow.run(
                os.path.join(hydra.utils.get_original_cwd(), "src", "data_ingestion"),
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

    
if __name__ == "__main__":
    go()
