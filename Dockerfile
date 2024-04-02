# Use the official Miniconda3 image as base
FROM continuumio/miniconda3:latest

# Set working directory in the container
WORKDIR /app

# Copy the environment file into the container
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Activate the conda environment
SHELL ["conda", "run", "-n", "stock_predictor", "/bin/bash", "-c"]


# Copy the rest of the application code into the container
COPY . .

# Initialize the Airflow database
RUN airflow db init

# Set the DAGs folder path in the Airflow configuration
RUN sed -i 's|^dags_folder.*$|dags_folder = /app/airflow/dags|' ~/airflow/airflow.cfg
RUN sed -i 's|^load_examples.*$|load_examples = False|' ~/airflow/airflow.cfg
RUN sed -i 's|^dags_are_paused_at_creation.*$|dags_are_paused_at_creation = False|' ~/airflow/airflow.cfg

# Configure Airflow authentication
RUN airflow users create \
    --username admin \
    --firstname admin \
    --lastname user \
    --role Admin \
    --email admin@example.com \
    --password admin
    
# Expose the port for Streamlit
EXPOSE 8080 8501

# Command to run Streamlit
#CMD ["conda", "run", "-n", "stock_predictor", "streamlit", "run", "dashboard.py"]

CMD ["sh", "-c", "conda run -n stock_predictor airflow webserver -p 8080 & conda run -n stock_predictor airflow scheduler & conda run -n stock_predictor streamlit run dashboard.py"]