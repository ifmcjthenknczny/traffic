#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traffic
Created on Wed Aug 11 14:57:23 2021
@author: mcj
"""

import time

from datetime import datetime, timedelta
from config import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from consts import LOGO, WEEKDAYS
from helpers import *

def start_later(time_string):
    time_now = datetime.now()
    planned_time = time_string.split(":")

    planned_hour = int(planned_time[0]) % 24
    planned_minutes = int(planned_time[1])
    planned_seconds = 0

    now_hour, now_minutes, now_seconds = time_now_to_array(time_now)

    if planned_hour == now_hour:
        if planned_minutes <= now_minutes:
            planned_hour += 24
    elif planned_hour < now_hour:
        planned_hour += 24

    planned_time = [planned_hour, planned_minutes, planned_seconds]

    time_to_wait = 3600*(planned_hour - now_hour) + 60 * \
        (planned_minutes - now_minutes) + (planned_seconds - now_seconds)
    hours_string = timedelta(seconds=time_to_wait)

    print("\nWaiting", hours_string, "Starting script at", time_string)

    if MAKE_SURE_IT_IS_WAITING:
        while time_to_wait > 600:
            time.sleep(600)
            time_to_wait = time_to_wait - 600
            hours_string = timedelta(seconds=time_to_wait)
            print("Still here! ", hours_string, "left to start!")

    time.sleep(time_to_wait)

print(LOGO)

CSV_BACKUP_NAME = CSV_NAME.replace('.csv', '_backup.csv')

if REPEAT:
    print("Time interval, repeat work mode")
else:
    print("Continous work mode")

if FORCED_START_NOW == False:
    print("Start time:", START_TIME)
elif FORCED_START_NOW == False and REPEAT == True:
    print("Start time in second cycle:", START_TIME)
if REPEAT:
    print("End time:", END_TIME)
print("\n")

while True:
    if FORCED_START_NOW == False:
        start_later(START_TIME)

    FORCED_START_NOW = False

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(
        "--incognito --disable-extensions --disable-notifications --disable-infobars --headless --log-level=3")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(GOOGLE_MAPS_URL)

    consent_button = driver.find_elements(By.TAG_NAME,
        "button")[2]
    consent_button.click()
    page_title = driver.title.split("–")[0]

    results_list = []

    init_csv(CSV_NAME, CSV_BACKUP_NAME, page_title)

    delta_time_first_previous = datetime.now()
    print("\nJust started at", datetime.now().strftime("%H:%M"),
          "! Interval of reporting:", INTERVAL_MINUTES, "minutes.")

    while True:
        delta_time = datetime.now()
        time_now = delta_time.strftime("%H:%M")
        day_now = delta_time.strftime("%Y-%m-%d")
        weekday = WEEKDAYS[delta_time.weekday()]

        if REPEAT:
            try:
                if END_TIME.split(':') == time_now.split(':'):
                    print("Webscraping reached endtime.")
                    break
            except:
                pass

        if is_time_to_update(delta_time_first_previous, delta_time, INTERVAL_MINUTES):
            update_csv_file(calculate_avg_result_row(results_list, weekday, day_now),
                           CSV_NAME, CSV_BACKUP_NAME)
            delta_time_first_previous = datetime.now()
            results_list = []

        try:
            elem = driver.find_element(By.XPATH, 
                '//*[@id="section-directions-trip-0"]/div/div[1]/div[1]/div[1]/span[1]').text
            traffic_time = split_time(elem)
        except:
            driver.refresh()
            continue

        result = [weekday, day_now, time_now, str(traffic_time)]
        results_list += [result]

        time.sleep(SLEEP_TIME)
        driver.refresh()

    if REPEAT == False:
        break
