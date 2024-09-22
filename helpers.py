import csv
import shutil
from config import *
from datetime import datetime
from consts import LOGO, WEEKDAYS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def update_csv_file(new_result, csv_filename, db_backup_name):
    with open(csv_filename, 'a', newline='\n') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=";", quotechar='|')
        data_writer.writerow(new_result)
    if ENABLE_RAPORTING:
        print(new_result[-3], "-", new_result[-2], ":",
              round(float(new_result[-1].replace(',', '.')), 1), " min")


def is_time_to_update(time_first, time_now, interval):
    minutes_now = time_now.minute
    minutes_first = time_first.minute
    hours_now = time_now.hour
    hours_first = time_first.hour

    minutes_now += 60 * (hours_now - hours_first)

    if minutes_now - minutes_first >= interval:
        return True
    else:
        return False


def calculate_avg_result_row(results_list, weekday, day_now):
    first_time = results_list[0][2]
    last_time = results_list[-1][2]
    avg_traffic_time = sum([int(entry[-1]) for entry in results_list])/len(results_list)

    return [weekday, day_now, first_time, last_time, str(avg_traffic_time).replace(".", ",")]


def init_csv(csv_filename, csv_backup_filename, page_title):
    try:
        shutil.copyfile(csv_filename, csv_backup_filename)
    except FileNotFoundError:
        open(csv_filename, 'w', newline='\n')
    with open(csv_filename, 'a', newline='\n') as csv_file:
        starter_writer = csv.writer(csv_file, delimiter=";", quotechar='|')
        starter_writer.writerow('')
        starter_writer.writerow([page_title])
        starter_writer.writerow([datetime.now().strftime("%Y-%m-%d")])

def time_now_to_array(time_now):
    now_hour = int(time_now.hour)
    now_minutes = int(time_now.minute)
    now_seconds = int(time_now.second)
    return [now_hour, now_minutes, now_seconds]


def calculate_difference_seconds(now_time, planned_time):
    planned_hour, planned_minutes, planned_seconds = planned_time
    now_hour, now_minutes, now_seconds = now_time
    return 3600*(planned_hour - now_hour) + 60*(planned_minutes - now_minutes) + (planned_seconds - now_seconds)

def calculate_time_minutes(time_element):
    time_element = time_element.split()
    if len(time_element) == 2:
        if time_element[1] == "min":
            traffic_time = int(time_element[0])
        elif time_element[1] == "godz.":
            traffic_time = int(time_element[0])*60
    elif len(time_element) == 4:
        if time_element[1] == "godz.":
            traffic_time = int(time_element[0])*60 + int(time_element[2])
    return traffic_time

def print_starting_window():
    print(LOGO)

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

def init_driver():
    chrome_options = webdriver.ChromeOptions()
    arguments = "--incognito --disable-extensions --disable-notifications --disable-infobars --log-level=3 --headless"
    chrome_options.add_argument(arguments)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(GOOGLE_MAPS_URL)

    consent_button = driver.find_elements(By.TAG_NAME,
        "button")[2]
    consent_button.click()
    return driver

def extract_datetime_data(datetime):
    time_now = datetime.strftime("%H:%M")
    day_now = datetime.strftime("%Y-%m-%d")
    weekday = WEEKDAYS[datetime.weekday()]
    return weekday, day_now, time_now