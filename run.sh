#!/bin/bash

source $HOME/miniconda/etc/profile.d/conda.sh
conda activate stock_predictor
streamlit run dashboard.py
