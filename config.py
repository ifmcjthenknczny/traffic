START_TIME = "06:00" #hour of start HH:MM
FORCED_START_NOW = False #forces starting now True/False

END_TIME = '10:00' #hour of end HH:MM. Works if REPEAT = True
REPEAT = True #True: repeat every day in given hours, False: work continuously

ENABLE_RAPORTING = True #console logging travel time right now
INTERVAL_MINUTES = 5 #reporting and result averaging interval (in minutes)
SLEEP_TIME = 5 #seconds after query to google maps is repeated

#prints out every 10 minutes confirmation that program is waiting if not started already, True/False
MAKE_SURE_IT_IS_WAITING = True 

#link to google maps with given road
GOOGLE_MAPS_URL = "https://www.google.pl/maps/dir/New+York,+Nowy+Jork,+Stany+Zjednoczone/Vancouver,+Kolumbia+Brytyjska,+Kanada/@52.4212778,16.854469,13z/data=!4m11!4m10!1m2!1m1!1s0x89c24fa5d33f083b:0xc80b8f06e177fe62!1m5!1m1!1s0x548673f143a94fb3:0xbb9196ea9b81f38b!2m2!1d-123.1207375!2d49.2827291!3e0?entry=ttu&g_ep=EgoyMDI0MDkxNi4wIKXMDSoASAFQAw%3D%3D"

#name of output csv file
CSV_NAME = "traffic_time.csv"