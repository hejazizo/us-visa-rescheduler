# Visa Rescheduler
Python code to re-schedule US VISA (ais.usvisa-info.com) appointments automatically.

## Prerequisites
- Having a US VISA appointment scheduled already.
- Google Chrome installed (to be controlled by the script).
- Python installed (for running the script).

## Installation
Install the required python packages by running:
```bash
pip install -r requirements.txt
```

## Configuration
Update the `config.ini` file with all the details required such as sign in email, password, schedule ID, etc. You can find these details in the URL of the appointment page.
For example if your appointment URL is https://ais.usvisa-info.com/en-ca/niv/groups/99999999, then:
- `COUNTRY_CODE` = en-ca
- `SCHEDULE_ID` = 99999999

`MY_SCHEDULE_DATE` the furthest date you want to check for. The format is YYYY-MM-DD, for example 2023-01-30 for January 30, 2023 means that the script will check for appointments until January 30, 2023 to reschedule your appointment to the earliest available date.

`FACILITY_ID` is the location of the appointment. You have to check it through the dropdown menu on the US Visa website in rescheduling. Click on the cities dropdown menu, click inspect element, and find the value of the selected location
Last I checked, for Canada, the values are:
- Calgary: 89
- Halifax: 90
- Montreal: 91
- Ottawa: 92
- Quebec City: 93
- Toronto: 94
- Vancouver: 95

![Facility ID](./images/facility_id.png)

`CHROMEDRIVER` section has details about the Chrome browser. If you are running the code locally, you don't need to change anything here.

If you want to reschedule and check multiple locations, you can run the script multiple times with different `FACILITY_ID` values. For example, if you want to check for appointments in Toronto and Vancouver, you can run the script twice with `FACILITY_ID` set to 94 and 95 respectively.

We have a plan to add support for multiple locations in the future. Stay tuned!

## How to Run
1. `cd` into the main directory where the requirements.txt file is located.
2. Run `export PYTHONPATH=$PYTHONPATH:$(pwd)` to add the current directory to the python path.
3. Run `python src/main.py` to start the script.
4. The script will open a Chrome window and start the re-scheduling process.
5. Once the re-scheduling is done, the script will close the Chrome window.
