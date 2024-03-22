#!/bin/bash

source $HOME/miniconda/bin/activate
conda activate stock_predictor
streamlit run dashboard.py
