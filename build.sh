#!/bin/bash

# Check if Miniconda is already installed
if [ ! -d "$HOME/miniconda" ]; then
    # Install Miniconda
    echo ""
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda
fi;

# Add Miniconda binaries to PATH
# export PATH="$HOME/miniconda/bin:$PATH";
echo PATH="\$HOME/miniconda/bin:\$PATH" >> ~/.bashrc
cat ~/.bashrc
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>> HERE"
whoami
#source /root/.bashrc
# Activate Conda environment
source $HOME/miniconda/etc/profile.d/conda.sh;

# # Check if Conda environment exists, create if not
# if ! conda env list | grep -q "stock_predictor"; then
#     # Create Conda environment from environment.yml
#     conda env create -f environment.yml
# fi;

# # Activate the Conda environment
# conda activate stock_predictor;

# # # Verify Conda environment
# # conda info --envs

# # Function to search for Miniconda installation directory recursively
# search_miniconda() {
#     # Search for Miniconda directory in all files within the system
#     MINICONDA_PATH=$(find / -type d -name "miniconda" 2>/dev/null | grep -E "/miniconda$")
    
#     if [ -n "$MINICONDA_PATH" ]; then
#         echo "Miniconda is installed at: $MINICONDA_PATH"
#     else
#         echo "Miniconda is not installed."
#     fi
# }

# # Execute the function to search for Miniconda
# search_miniconda