import json
import random
import sys
import time
from datetime import datetime
from typing import Union

import emoji
import requests
from loguru import logger
from prettytable import PrettyTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

from src.constants import COOLDOWN_TIME, EXCEPTION_TIME, RETRY_TIME, STEP_TIME
from src.utils import get_driver, load_config, my_condition

config = load_config('src/config.ini')
USERNAME = config['USVISA']['USERNAME']
PASSWORD = config['USVISA']['PASSWORD']
SCHEDULE_ID = config['USVISA']['SCHEDULE_ID']
MY_SCHEDULE_DATE = config['USVISA']['MY_SCHEDULE_DATE']
COUNTRY_CODE = config['USVISA']['COUNTRY_CODE']
LOCAL_USE = config['CHROMEDRIVER'].getboolean('LOCAL_USE')
HUB_ADDRESS = config['CHROMEDRIVER']['HUB_ADDRESS']
FACILITY_ID = sys.argv[1] if len(sys.argv) > 1 else config['USVISA']['FACILITY_ID']
DATE_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment/days/{FACILITY_ID}.json?appointments[expedite]=false"
TIME_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment/times/{FACILITY_ID}.json?date=%s&appointments[expedite]=false"
APPOINTMENT_URL = f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv/schedule/{SCHEDULE_ID}/appointment"
GREEN_CIRCLE_EMOJI = emoji.emojize(':green_circle:')
RED_CIRCLE_EMJOI = emoji.emojize(':red_circle:')
MAX_DATE_COUNT = 5


driver = get_driver(local_use=LOCAL_USE, hub_address=HUB_ADDRESS)

def login():
    """
    Login to the US Visa appointment system.
    """
    # Open the Appointments service page for the country
    driver.get(f"https://ais.usvisa-info.com/{COUNTRY_CODE}/niv")
    time.sleep(STEP_TIME)

    # Click on Continue application
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(STEP_TIME)

    logger.info("Login start...")
    href = driver.find_element(
        By.XPATH, '//*[@id="header"]/nav/div/div/div[2]/div[1]/ul/li[3]/a')
    href.click()
    time.sleep(STEP_TIME)
    Wait(driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))

    logger.info("Click bounce...")
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(STEP_TIME)

    # Fill the form
    logger.info("Input email...")
    user = driver.find_element(By.ID, 'user_email')
    user.send_keys(USERNAME)
    time.sleep(random.randint(1, 3))

    logger.info("Input password")
    pw = driver.find_element(By.ID, 'user_password')
    pw.send_keys(PASSWORD)
    time.sleep(random.randint(1, 3))

    logger.info("Click privacy...")
    box = driver.find_element(By.CLASS_NAME, 'icheckbox')
    box .click()
    time.sleep(random.randint(1, 3))

    logger.info("Commit...")
    btn = driver.find_element(By.NAME, 'commit')
    btn.click()
    time.sleep(random.randint(1, 3))

    # FIXME: This is not working for now to check if login is successful
    # Wait(driver, 60).until(
    #     EC.presence_of_element_located((By.XPATH, REGEX_CONTINUE))
    # )
    logger.info("Login successful!")


def get_available_dates():
    """
    Get the date of the next available appointments.
    """
    driver.get(DATE_URL)
    if not is_logged_in():
        login()
        return get_available_dates()
    else:
        content = driver.find_element(By.TAG_NAME, 'pre').text
        date = json.loads(content)
        return date


def get_valid_date(dates: list) -> Union[str, None]:
    """
    Get the first valid date from the list of available dates.
    A valid date is a date that is earlier than MY_SCHEDULE_DATE.

    :param dates: List of available dates
    """
    def is_earlier(date):
        my_date = datetime.strptime(MY_SCHEDULE_DATE, "%Y-%m-%d")
        new_date = datetime.strptime(date, "%Y-%m-%d")
        return my_date > new_date

    logger.info(f"Checking for a date earlier than {MY_SCHEDULE_DATE}...")
    dates_table = PrettyTable()
    dates_table.field_names = ["Available Date", "Business Day", "Is Earlier"]
    dates_table.align["Available Date"] = "l"
    dates_table.align["Business Day"] = "l"
    dates_table.align["Is Earlier"] = "c"
    for d in dates:
        date = d.get('date')
        _, month, day = date.split('-')
        dates_table.add_row([
            date,
            'Yes' if d.get('business_day') else 'No',
            GREEN_CIRCLE_EMOJI if is_earlier(date) else RED_CIRCLE_EMJOI,
        ])
    print(dates_table)

    for d in dates:
        date = d.get('date')

        # Check if date is earlier than my schedule date
        if not is_earlier(date):
            continue

        # TODO: Check if date meets my condition
        # This feature needs improvement, so it's disabled for now
        # and my_condition(month, day) always returns True
        _, month, day = date.split('-')
        if not my_condition(month, day):
            continue

        return date


def get_time(date):
    """
    Get the time of the next available appointments.

    :param date: Available date to get time
    :return: Time of the next available appointment.
    """
    time_url = TIME_URL % date
    driver.get(time_url)
    content = driver.find_element(By.TAG_NAME, 'pre').text
    data = json.loads(content)
    time = data.get("available_times")[-1]
    logger.info(f"Got time successfully! {date} {time}")
    return time


def reschedule(date: str) -> bool:
    """
    Reschedule the appointment.

    :param date: Available date to reschedule
    :return: The response of the reschedule request.
    """
    logger.info(f"Starting Reschedule ({date})")
    time = get_time(date)
    driver.get(APPOINTMENT_URL)

    data = {
        "utf8": driver.find_element(by=By.NAME, value='utf8').get_attribute('value'),
        "authenticity_token": driver.find_element(by=By.NAME, value='authenticity_token').get_attribute('value'),
        "confirmed_limit_message": driver.find_element(
            by=By.NAME, value='confirmed_limit_message'
        ).get_attribute('value'),
        "use_consulate_appointment_capacity": driver.find_element(
            by=By.NAME, value='use_consulate_appointment_capacity'
        ).get_attribute('value'),
        "appointments[consulate_appointment][facility_id]": FACILITY_ID,
        "appointments[consulate_appointment][date]": date,
        "appointments[consulate_appointment][time]": time,
    }

    headers = {
        "User-Agent": driver.execute_script("return navigator.userAgent;"),
        "Referer": APPOINTMENT_URL,
        "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
    }

    r = requests.post(APPOINTMENT_URL, headers=headers, data=data)
    if r.text.find('Successfully Scheduled') != -1:
        logger.info(f"Rescheduled Successfully! {date} {time}")
        return True

    logger.info(f"Reschedule Failed. {date} {time}")
    return False


def is_logged_in():
    content = driver.page_source
    return content.find('error') == -1


def search_for_available_date():
    """
    Search for available appointment date and reschedule if found.

    :return: True if reschedule successfully, otherwise call itself again.
    """
    logger.info("Searching for available date...")
    dates = get_available_dates()[:MAX_DATE_COUNT]
    if not dates:
        logger.info(f"No available date, retrying in {RETRY_TIME} seconds...")
        time.sleep(RETRY_TIME)
        return search_for_available_date()

    date = get_valid_date(dates)
    if date:
        if reschedule(date):
            logger.info("Reschedule successfully!")
            return True
        else:
            logger.info(f"Reschedule failed, retrying in {COOLDOWN_TIME} seconds...")
            time.sleep(COOLDOWN_TIME)

    logger.info(f"No earlier date, retrying in {RETRY_TIME} seconds...")
    time.sleep(RETRY_TIME)
    return search_for_available_date()


if __name__ == "__main__":
    login()
    RETRY_COUNT = 0
    MAX_RETRY = 3

    while True:
        if RETRY_COUNT > MAX_RETRY:
            break

        try:
            if search_for_available_date():
                break
        except Exception as e:
            RETRY_COUNT += 1
            logger.error(e)
            logger.error(f"Exception occurred, retrying after {EXCEPTION_TIME} seconds...")
            time.sleep(EXCEPTION_TIME)
