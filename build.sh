#!/bin/bash

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

# Add the conda binary directory to PATH
export PATH=~/miniconda3/bin:$PATH

# Source the shell initialization scripts to ensure PATH changes take effect
source ~/.bashrc
source ~/.zshrc

echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# Now the conda command should be available
conda --version

# Check if Conda environment exists, create if not
if ! conda env list | grep -q "stock_predictor"; then
    # Create Conda environment from environment.yml
    echo ">>>>>>>>>>>>>>> HERE"
    conda env create -f environment_test.yml
fi;

conda info --envs
# # Activate the Conda environment
conda activate stock_predictor;

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