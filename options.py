STARTTIME = "13:30" #hour of start HH:MM
FORCEDSTARTNOW = False #forces starting now True/False

ENDTIME = '16:30' #hour of end HH:MM. Works if REPEAT = True
REPEAT = True #True: repeat every day in given hours, False: work continuously

RAPORTING = True #console logging travel time right now
INTERVALMINUTES = 5 #reporting and result averaging interval (in minutes)
SLEEPTIME = 10 #seconds after query to google maps is repeated

#prints out every 10 minutes confirmation that program is waiting if not started already, True/False
MAKESUREITISWAITING = True 

#link to google maps with given road
LINK = "https://www.google.pl/maps/dir/Pa%C5%82ac+Kultury+i+Nauki,+plac+Defilad,+Warszawa/Lotnisko+Chopina,+%C5%BBwirki+i+Wigury,+Warszawa/@52.1825485,20.9132382,12z/data=!4m14!4m13!1m5!1m1!1s0x471ecc8c92692e49:0xc2e97ae5311f2dc2!2m2!1d21.005995!2d52.231838!1m5!1m1!1s0x4719331c42e95ce3:0x22c5f5a26843e8d1!2m2!1d20.9678911!2d52.1672369!3e0"

#name of output database
DBASENAME = "trafficTime.csv"