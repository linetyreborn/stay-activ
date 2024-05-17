#!/bin/bash

# Log file path
log_file="install_and_create_shortcut.log"

# Function to log messages
log_message() {
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $1" >> "$log_file"
}

# Log script start
log_message "Script started"

# Check if Python is installed
if ! command -v python &> /dev/null
then
    log_message "Error: Python is not installed."
    exit 1
fi

# Install the required packages
pip install -r requirements.txt

# Path to your Python script (app.py)
script_path=$(realpath app.py)

# Path to the startup folder
startup_folder=$(powershell.exe -Command "[Environment]::GetFolderPath('Startup')")

# Create a shortcut name based on the script name
shortcut_name=$(basename "$script_path" .py).lnk

# Create a shortcut to the script in the startup folder
shortcut_path="$startup_folder/$shortcut_name"
powershell.exe -Command "(New-Object -ComObject WScript.Shell).CreateShortcut('$shortcut_path').TargetPath = '$script_path'"

log_message "Shortcut created at $shortcut_path"

# Log script end
log_message "Script completed"