#!/bin/bash

# Check if Miniconda is already installed
if [ ! -d "$HOME/miniconda" ]; then
    # Install Miniconda
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
fi

# Add Miniconda binaries to PATH
export PATH="$HOME/miniconda/bin:$PATH"

# Activate Conda environment
source $HOME/miniconda/etc/profile.d/conda.sh


Check if Conda environment exists, create if not
if ! conda env list | grep -q "stock_predictor"; then
    # Create Conda environment from environment.yml
    conda env create -f environment.yml
fi

Activate the Conda environment
conda activate stock_predictor

# # Verify Conda environment
# conda info --envs
