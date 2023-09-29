### Setup Python Environment

Within the project root directory
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
pip install -e .

# Run sample scripts
python sample/led_effect.py
```
