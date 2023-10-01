### Setup Python Environment

Within the project root directory. To run on the raspberry pi, python commands
must be run with `sudo python3`.
```
# Install virtualenv
python3 -m pip install virtualenv

# Create virtual environment
virtualenv env

# Activate the project environment
source env/bin/activate

# Install all project dependencies
python3 -m pip install -r requirements.txt

# Install all local packages
# This command must be run every time a change is made to the led directory when
# running python as sudo.
python3 -m pip install -e .

# Run sample scripts
python3 sample/led_effect.py
```
