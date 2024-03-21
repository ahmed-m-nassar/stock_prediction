#!/bin/bash

# Activate the Conda environment
source $HOME/miniconda/etc/profile.d/conda.sh  # Ensure conda commands are available
conda activate stock_predictor

# Run the Streamlit app
streamlit run dashboard.py
