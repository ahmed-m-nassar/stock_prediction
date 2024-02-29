import pandas as pd
import wandb
import logging

logger = logging.getLogger(__name__)


def read_data_from_wandb(run , artifact_name , download_path):
    """
    Read ingested data from Weights & Biases.

    Parameters:
        artifact_name (str): The name of the artifact containing the ingested data.

    Returns:
        pd.DataFrame: The DataFrame containing the ingested data.
    """
    try:
        logger.info(f"Reading data from W&B artifact: {artifact_name}")
        artifact = run.use_artifact(artifact_name)
        artifact_dir = artifact.download(root = download_path)
        file_name = artifact_name.split(':')[0]
        df = pd.read_csv(f"{artifact_dir}/{file_name}.csv")
        logger.info("Data read successfully")
        return df
    except Exception as e:
        logger.error(f"Error occurred while reading data from W&B: {str(e)}")
        raise ValueError(f"Failed to read data from W&B artifact: {str(e)}")

def upload_data_to_wandb(run , data_path , output_artifact, output_type, output_description):
    """
    Upload data to Weights & Biases.

    Parameters:
    - input_data (pd.DataFrame): Input DataFrame containing the cleaned data.
    - output_artifact (str): Name of the artifact for the cleaned data.
    - output_type (str): Type of the output data artifact.
    - output_description (str): Description of the output data artifact.
    """
    try:
        logger.info(f"Uploading data to W&B artifact: {output_artifact}")
    
        artifact = wandb.Artifact(
        output_artifact,
        type=output_type,
        description=output_description,
        )

        artifact.add_file(data_path)
        run.log_artifact(artifact)
        
        logger.info("Data uploaded successfully")
    except Exception as e:
        logger.error(f"Error occurred while uploading data to W&B: {str(e)}")
        raise ValueError(f"Failed to upload data to W&B: {str(e)}")
