#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Traffic
Created on Wed Aug 11 14:57:23 2021
@author: mcj
"""

import csv
import shutil
import time

from datetime import datetime, timedelta
from options import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def getTimeNow(timeNow):
    nowHour = int(timeNow.hour)
    nowMinutes = int(timeNow.minute)
    nowSeconds = int(timeNow.second)
    return [nowHour, nowMinutes, nowSeconds]


def timeDifference(nowTime, plannedTime):
    plannedHour, plannedMinutes, plannedSeconds = plannedTime
    nowHour, nowMinutes, nowSeconds = nowTime
    return 3600*(plannedHour - nowHour) + 60*(plannedMinutes - nowMinutes) + (plannedSeconds - nowSeconds)


def startLater(timeString):
    timeNow = datetime.now()
    plannedTime = timeString.split(":")

    plannedHour = int(plannedTime[0]) % 24
    plannedMinutes = int(plannedTime[1])
    plannedSeconds = 0

    nowHour, nowMinutes, nowSeconds = getTimeNow(timeNow)

    if plannedHour == nowHour:
        if plannedMinutes <= nowMinutes:
            plannedHour += 24
    elif plannedHour < nowHour:
        plannedHour += 24

    plannedTime = [plannedHour, plannedMinutes, plannedSeconds]

    timeToWait = 3600*(plannedHour - nowHour) + 60 * \
        (plannedMinutes - nowMinutes) + (plannedSeconds - nowSeconds)
    hourString = timedelta(seconds=timeToWait)

    print("\nWaiting", hourString, "Starting script at", timeString)

    if MAKESUREITISWAITING:
        while timeToWait > 600:
            time.sleep(600)
            timeToWait = timeToWait - 600
            hourString = timedelta(seconds=timeToWait)
            print("Still here! ", hourString, "left to start!")

    time.sleep(timeToWait)


def splitTime(elem):
    elem = elem.split()
    if len(elem) == 2:
        if elem[1] == "min":
            trafficTime = int(elem[0])
        elif elem[1] == "godz.":
            trafficTime = int(elem[0])*60
    elif len(elem) == 4:
        if elem[1] == "godz.":
            trafficTime = int(elem[0])*60 + int(elem[2])
    return trafficTime


def updateDatabase(newResult, databaseName, databaseBackupName):
    # po każdym wznowieniu robić linię przerwy dla czytelnosci w csv
    with open(databaseName, 'a', newline='\n') as csvfile:
        dataWriter = csv.writer(csvfile, delimiter=";", quotechar='|')
        dataWriter.writerow(newResult)
    if RAPORTING:
        print(newResult[-3], "-", newResult[-2], ":",
              round(float(newResult[-1].replace(',', '.')), 1), " min")


def timeToUpdate(timeFirst, timeNow, interval):
    minutesNow = timeNow.minute
    minutesFirst = timeFirst.minute
    hoursNow = timeNow.hour
    hoursFirst = timeFirst.hour

    minutesNow += 60 * (hoursNow - hoursFirst)

    if minutesNow - minutesFirst >= interval:
        return True
    else:
        return False


def giveAveragedResult(resultsList):
    firstTime = resultsList[0][2]
    lastTime = resultsList[-1][2]
    averageTrafficTime = sum([int(entry[-1])
                             for entry in resultsList])/len(resultsList)

    return [weekday, dayNow, firstTime, lastTime, str(averageTrafficTime).replace(".", ",")]


def startDatabase(databaseName, databaseBackupName):
    try:
        shutil.copyfile(databaseName, databaseBackupName)
    except FileNotFoundError:
        open(databaseName, 'w', newline='\n')
    with open(databaseName, 'a', newline='\n') as csvfile:
        starterWriter = csv.writer(csvfile, delimiter=";", quotechar='|')
        starterWriter.writerow('')
        starterWriter.writerow([pageTitle])
        starterWriter.writerow([datetime.now().strftime("%Y-%m-%d")])


print("\n\n_/_/_/_/_/  _/_/_/      _/_/    _/_/_/_/  _/_/_/_/  _/_/_/    _/_/_/   \n   _/      _/    _/  _/    _/  _/        _/          _/    _/          \n  _/      _/_/_/    _/_/_/_/  _/_/_/    _/_/_/      _/    _/           \n _/      _/    _/  _/    _/  _/        _/          _/    _/            \n_/      _/    _/  _/    _/  _/        _/        _/_/_/    _/_/_/\n")

DBASEBACKUPNAME = DBASENAME.replace('.csv', '_backup.csv')

if REPEAT:
    print("Time interval, repeat work mode")
else:
    print("Continous work mode")

if FORCEDSTARTNOW == False:
    print("Start time:", STARTTIME)
elif FORCEDSTARTNOW == False and REPEAT == True:
    print("Start time in second cycle:", STARTTIME)
if REPEAT:
    print("End time:", ENDTIME)
print("\n")

while True:

    if FORCEDSTARTNOW == False:
        startLater(STARTTIME)

    FORCEDSTARTNOW = False

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument(
        "--incognito --disable-extensions --disable-notifications --headless --disable-infobars --log-level=3")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chromeOptions)
    driver.get(LINK)

    consentButton = driver.find_element_by_xpath(
        "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button")
    consentButton.click()
    pageTitle = driver.title.split("–")[0]

    weekdays = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
    resultsList = []

    startDatabase(DBASENAME, DBASEBACKUPNAME)

    dTimeFirstPrevious = datetime.now()
    print("\nJust started at", datetime.now().strftime("%H:%M"),
          "! Interval of reporting:", INTERVALMINUTES, "minutes.")

    while True:
        dTime = datetime.now()
        timeNow = dTime.strftime("%H:%M")
        dayNow = dTime.strftime("%Y-%m-%d")
        weekday = weekdays[dTime.weekday()]

        if REPEAT:
            try:
                if ENDTIME.split(':') == timeNow.split(':'):
                    print("Webscraping reached endtime.")
                    break
            except:
                pass

        if timeToUpdate(dTimeFirstPrevious, dTime, INTERVALMINUTES):
            updateDatabase(giveAveragedResult(resultsList),
                           DBASENAME, DBASEBACKUPNAME)
            dTimeFirstPrevious = datetime.now()
            resultsList = []

        try:
            elem = driver.find_element_by_xpath(
                '//*[@id="section-directions-trip-0"]/div/div[1]/div[1]/div[1]/span[1]').text
            trafficTime = splitTime(elem)
        except:
            driver.refresh()
            continue

        result = [weekday, dayNow, timeNow, str(trafficTime)]
        resultsList += [result]

        time.sleep(SLEEPTIME)
        driver.refresh()

    if REPEAT == False:
        break
