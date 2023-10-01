### Setup Python Environment

#### Development Environment 
Within the project root directory.
```
# Install virtualenv
pip install virtualenv

# Create virtual environment
virtualenv env

# Activate the project environment
source env/bin/activate

# Install all project dependencies
pip install -r requirements.txt

# Install all local packages
# This command must be run every time a change is made to the led directory when
# running python as sudo.
pip install -e .

# Run sample scripts
python sample/led_effect.py
```

#### Raspberry Pi LED Environment

Within the project root directory.
```
# Install all project dependencies
python3 -m pip install -r requirements_rpi.txt

# Install all local packages
sudo python3 -m pip install -e .

# Run sample scripts
sudo python3 sample/led_effect.py
```