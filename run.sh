#!/bin/bash

# source $HOME/miniconda/bin/activate
eval "$(conda shell.bash hook)"
conda activate stock_predictor
streamlit run dashboard.py
