#!/bin/bash

# Function to search for Miniconda installation directory recursively
search_miniconda() {
    # Search for Miniconda directory in all files within the system
    MINICONDA_PATH=$(find / -type d -name "miniconda" 2>/dev/null | grep -E "/miniconda$")
    
    if [ -n "$MINICONDA_PATH" ]; then
        echo "Miniconda is installed at: $MINICONDA_PATH"
    else
        echo "Miniconda is not installed."
    fi
}

# Execute the function to search for Miniconda
search_miniconda
# source $HOME/miniconda/bin/activate
# eval "$(conda shell.bash hook)"
# conda activate stock_predictor
# streamlit run dashboard.py
