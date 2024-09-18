import schedule
import time
from threading import Thread

import setup_database
from server import start_server

from bar_chart import chart
from clear_old_data import remove_data_before_last_x_days
from pinger import ping_and_record

schedule.every(30).seconds.do(ping_and_record)
schedule.every(1).minutes.do(chart)
schedule.every().day.at("00:00").do(remove_data_before_last_x_days, 2)

while True:
    thread = Thread(target=start_server)
    thread.start() # start the server in a separate thread
    schedule.run_pending()
    time.sleep(5)