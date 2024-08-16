import unittest
import sys, os
sys.path.append(os.path.abspath("./src"))

from datetime import datetime, timedelta

import bar_chart
import db_connector
import clear_old_data

class TestClearData(unittest.TestCase):
    def test_clear_old_data(self):
        date_time_out_of_date = (datetime.now() + timedelta(weeks=-1)).strftime("%F %T")
        date_time_in_date = (datetime.now() + timedelta(days=-2)).strftime("%F %T")

        connection = db_connector.create_connection(":memory:") # creates DB in memory

        if connection:
            cursor = connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)")
            cursor.execute("INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 0)", (date_time_in_date,))
            cursor.execute("INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 0)", (date_time_out_of_date,))
            connection.commit()


            data = bar_chart.get_data_from_DB(200, connection) # get data from last 200 hours (i.e. just over a week)
            self.assertEqual(len(data), 2) # check two entries in DB before clearing

            clear_old_data.remove_data_before_last_x_days(3, connection)
            data = bar_chart.get_data_from_DB(200, connection)  # get data from last 200 hours (i.e. just over a week)

            self.assertEqual(len(data), 1) # check only one entry in Db after clearing
            connection.close()

if __name__ == '__main__':
    unittest.main()