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
from selenium.webdriver.common.by import By
from consts import X_PATHS
from helpers import update_csv_file, is_time_to_update, calculate_avg_result_row, init_csv, time_now_to_array, calculate_time_minutes, print_starting_window, init_driver, extract_datetime_data

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

CSV_BACKUP_NAME = CSV_NAME.replace('.csv', '_backup.csv')

print_starting_window()

while True:
    if FORCED_START_NOW == False:
        start_later(START_TIME)

    FORCED_START_NOW = False

    driver = init_driver()
    page_title = driver.title.split("–")[0]

    results_list = []
    init_csv(CSV_NAME, CSV_BACKUP_NAME, page_title)

    datetime_previous = datetime.now()
    print("\nJust started at", datetime.now().strftime("%H:%M"),
          "! Interval of reporting:", INTERVAL_MINUTES, "minutes.")

    while True:
        datetime_now = datetime.now()
        weekday, day_now, time_now = extract_datetime_data(datetime_now)

        if REPEAT:
            try:
                if END_TIME.split(':') == time_now.split(':'):
                    print("Webscraping reached endtime.")
                    break
            except:
                pass

        if is_time_to_update(datetime_previous, datetime_now, INTERVAL_MINUTES):
            avg_result_row = calculate_avg_result_row(results_list, weekday, day_now)
            update_csv_file(avg_result_row,
                            CSV_NAME, CSV_BACKUP_NAME)
            datetime_previous = datetime.now()
            results_list = []

        try:
            time_labels = [driver.find_element(By.XPATH, x_path).text for x_path in X_PATHS]
            traffic_time = min([calculate_time_minutes(label) for label in time_labels])
        except:
            driver.refresh()
            continue

        result = [weekday, day_now, time_now, str(traffic_time)]
        results_list += [result]

        time.sleep(SLEEP_TIME)
        driver.refresh()

    if REPEAT == False:
        break
