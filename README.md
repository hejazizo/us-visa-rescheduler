<img src="./images/logo.png" width="500" style="display: block; margin-left: auto; margin-right: auto;">

# Visa Rescheduler
Python code to re-schedule US VISA (ais.usvisa-info.com) appointments automatically.
This script is provided by [Pytopia](https://pytopia.ai/) team, and is not affiliated with the US VISA website.
Feel free to use this code for non-commercial purposes only. See the [License](#license) section for more details.

**WARNING: There is a limit for re-scheduling attempts.** Be careful not to exceed the limit. I did some research, some people say it's 3 attempts, some say it's 5 attempts. I don't know for sure. So be careful! I did 4 attempts and it worked for me.

Also be careful for refreshing the page too many times. If you refresh the page too many times, you will get a message saying that you have exceeded the limit of refreshing the page. I don't know the exact number of refreshes, but I put 10 minutes between each refresh, and had it running for 3 different locations. So like 3 minutes for each location. I even got the forbidden message. But don't worry, you are not banned forever. Just wait for a few hours and try again.

I could get an appointment that was scheduled for 2 days later, after running the script for 3 weeks. My previous appointment was scheduled for 1 year later. So it's worth it to run the script for a long time.


Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Disclaimer](#disclaimer)
- [License](#license)
- [Acknowledgments](#acknowledgments)

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

# Disclaimer
This script is provided as is. We are not responsible for any damage caused by using this script. Use at your own risk.

# License
This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License - see the [LICENSE](./LICENCE) file for details. You can use this code for non-commercial purposes only.

# Acknowledgments
- [Selenium](https://www.selenium.dev/) for automating the browser.
- [ChromeDriver](https://chromedriver.chromium.org/) for controlling Chrome.

If you enjoyed this project, please consider giving it a star ⭐️ and sharing it with your friends.
Also feel free to contribute to this project by creating a pull request.

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
