# Visa Rescheduler
Python code to re-schedule US VISA (ais.usvisa-info.com) appointments automatically.

## Prerequisites
- Having a US VISA appointment scheduled already.
- Google Chrome installed (to be controlled by the script).
- Python installed (for running the script).

## Installation
- Install the required python packages: `pip install -r requirements.txt`
- Update the `config.ini` file with all the details required

## How to Use
1. `cd` into the main directory where the requirements.txt file is located.
2. Run `export PYTHONPATH=$PYTHONPATH:$(pwd)` to add the current directory to the python path.
3. Run `python src/main.py` to start the script.
4. The script will open a Chrome window and start the re-scheduling process.
5. Once the re-scheduling is done, the script will close the Chrome window.
