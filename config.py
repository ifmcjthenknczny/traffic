from pydantic_settings import BaseSettings


class Config(BaseSettings):
    START_TIME: str = "06:00"  # hour of start HH:MM
    FORCED_START_NOW: bool = False  # forces starting now
    END_TIME: str = "10:00"  # hour of end HH:MM. Works if REPEAT = True
    REPEAT: bool = True  # True: repeat every day in given hours, False: work continuously
    ENABLE_RAPORTING: bool = True  # console logging travel time right now
    INTERVAL_MINUTES: int = 5  # reporting and result averaging interval (in minutes)
    SLEEP_TIME: int = 5  # seconds after query to google maps is repeated
    MAKE_SURE_IT_IS_WAITING: bool = (
        True  # prints out every 10 minutes confirmation that program is waiting if not started already, True/False
    )
    GOOGLE_MAPS_URL: str  # link to google maps with given road
    CSV_NAME: str = "traffic_time.csv"  # filename of output csv file

    class Config:
        env_file = ".env"


config = Config()
