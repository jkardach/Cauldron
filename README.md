## Setup Python Environment

### Development Environment 
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

### Raspberry Pi LED Environment

Within the project root directory.
```
# Install all project dependencies
python3 -m pip install -r requirements_rpi.txt

# Install all local packages
sudo python3 -m pip install -e .

# Run sample scripts
sudo python3 sample/led_effect.py
```

## Design

### UML Diagram
![UML Design](app/files/images/design.png)

The code currently follows the above design. Objects with similar colors all share the same base object type. The inheritance-heavy design allows us to define common behavior in base classes and to enable the use of mock objects. For example:

MockStrip uses a (NUM_PIXELS x 3) numpy array to represent an RGB LED strip. We can use the MockStrip anywhere an LedStrip is expected. This allows us to test LedEffects, which apply an effect on an LedStrip, without needing a physical LED strip.
