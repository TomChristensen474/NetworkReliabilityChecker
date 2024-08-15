import schedule
import time
import setup_database

from bar_chart import chart
from clear_old_data import remove_data_before_last_x_days
from pinger import ping_and_record

schedule.every(1).minutes.do(ping_and_record)
schedule.every(1).minutes.do(chart)
schedule.every().day.at("00:00").do(remove_data_before_last_x_days, 3)

while True:
    schedule.run_pending()
    time.sleep(1)