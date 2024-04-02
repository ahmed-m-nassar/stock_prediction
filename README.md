# End-to-End Machine Learning Pipeline for Stock Price Prediction

## Overview
This project implements an end-to-end machine learning pipeline for predicting stock price movements. 

The pipeline includes data ingestion, cleaning, feature engineering, training, and prediction scripts, all integrated with logging, documentation, and error handling.

Additionally, it utilizes various technologies such as Python, MLflow, Weights & Biases (wandb), Apache Airflow, Streamlit, Docker, and GitHub Actions.

## Features
- Data ingestion, cleaning, and feature engineering , training and prediction scripts
- Logging, documentation, and error handling
- Experiments and data management with wandb
- Scheduled prediction tasks with Apache Airflow
- Containerization with Docker
- CI/CD pipeline with GitHub Actions
- Visual interface with streamlit

## Usage
1. **Clone Repository:** 
   ```bash
   git clone <repository_url>
   cd <repository_directory>

2. **Build Docker Image:** 
   ```bash
   docker build -t stock-prediction .

3. **Run Docker Container** 
   ```bash
   docker run -p 8501:8501 -p 8080:8080 \
   -e WANDB_API_KEY=<Add your wandb api key> \
   -e DB_URL=<Add your db url> \
   stock-prediction

4. **Access Application** 
   ```bash
   http://localhost:8501 


5. **Access Airflow DAGs** 
   ```bash
   http://localhost:8080 

## Folder structure
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── artifacts
    │   ├── data_ingestion          <- Data from src/data_ingestion script.
    │   ├── data_cleaning           <- Data from src/data_cleaning script.
    │   ├── data_seggregation       <- Data from src/data_seggregation script.
    │   └── feature_engineering     
    │   └── prediction              <- Data from src/prediction script.
    │
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    │
    ├── environment.yml    <- The conda environment required to run the project
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data_ingestion          <- Scripts to download or generate data
    │   │   └── data_ingestion.py
    │   │
    │   ├── data_cleaning          <- Scripts to clean data
    │   │   └── data_cleaning.py
    │   │
    │   ├── data_seggregation       <- Scripts to split data
    │   │   └── data_seggregation.py
    │   │
    │   ├── feature_engineering          <- Scripts to create feature engineering pipeline
    │   │   └── feature_engineering.py  
    │   │
    │   ├── training          <- Scripts to train XGBOOST model
    │   │   └── training.py  
    │   │
    │   ├── prediction          <- Scripts to apply model on data and get prediction
    │   │   └── prediction.py  
    │   │
    │   ├── save_prediction          <- Scripts to save prediction in a database
    │   │   └── save_prediction.py  
    │   │
    │   ├── models          <- Trained Models
    │   │   
    │   ├── utils       <- utility scripts
    │   
    │   
    ├── unit_test                <- Unit tests scripts
       │
       │
       ├── data_ingestion          <- unit tests for src/data_ingestion/data_ingestion.py
       │   └── test_data_ingestion.py
       │
       │
       ├── data_cleaning          <- unit tests for src/data_cleaning/data_cleaning.py
       │   └── test_data_cleaning.py
       │
       │
       ├── data_seggregation          <- unit tests for src/data_seggregation/data_seggregation.py
       │   └── test_data_seggregation.py
       │
       │
       ├── feature_engineering          <- unit tests for src/feature_engineering/feature_engineering.py
       └── test_feature_engineering.py
   

--------