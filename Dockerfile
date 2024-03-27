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

# Expose the port for Streamlit
EXPOSE 8501

# Command to run Streamlit
CMD ["conda", "run", "-n", "stock_predictor", "streamlit", "run", "dashboard.py"]
