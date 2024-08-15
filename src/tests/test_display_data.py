import unittest
import sys, os
sys.path.append(os.path.abspath(".."))

from time import gmtime, strftime
from datetime import datetime, timedelta

from src import bar_chart
from src import db_connector


class TestDisplayData(unittest.TestCase):
    def testDisplayCodeNotError(self):
        date_time = (datetime.now()).strftime("%F %T")
        connection = db_connector.create_connection(":memory:") # creates DB in memory

        if connection:
            cursor = connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)")
            cursor.execute("INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 0)", (date_time,))
            connection.commit()
            
            data = bar_chart.get_data_from_DB(1, connection)

            try:
                bar_chart.render_data(data)
            except Exception as e:
                self.fail(f"Error: {e}")

            connection.close()


if __name__ == '__main__':
    unittest.main()