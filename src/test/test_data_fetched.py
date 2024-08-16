import unittest
import sys, os

sys.path.append(os.path.abspath("./src"))

from datetime import datetime, timedelta

import bar_chart
import db_connector


class TestFetchedData(unittest.TestCase):
    def test_dont_get_data_outside_timeframe(self):
        date_time = (datetime.now() + timedelta(hours=-3)).strftime("%F %T")
        print(date_time)

        connection = db_connector.create_connection(":memory:")  # creates DB in memory

        if connection:
            cursor = connection.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)"
            )
            cursor.execute(
                "INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 0)", (date_time,)
            )
            connection.commit()

            data = bar_chart.get_data_from_DB(1, connection)

            self.assertEqual(len(data), 0)
            connection.close()

    def test_get_data_inside_timeframe(self):
        date_time = (datetime.now()).strftime("%F %T")
        connection = db_connector.create_connection(":memory:")  # creates DB in memory

        if connection:
            cursor = connection.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)"
            )
            cursor.execute(
                "INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 0)", (date_time,)
            )
            connection.commit()

            data = bar_chart.get_data_from_DB(1, connection)

            self.assertEqual(len(data), 1)

            connection.close()

    def test_errors_if_DB_wrong_format(self):
        date_time = (datetime.now()).strftime("%F %T")
        connection = db_connector.create_connection(":memory:")  # creates DB in memory

        if connection:
            cursor = connection.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)"
            )
            cursor.execute(
                "INSERT INTO network_history VALUES(NULL, ?, ?, 0.3, 0)",
                (date_time, "i'm not a number"),
            )
            connection.commit()

            self.assertRaises(TypeError, bar_chart.get_data_from_DB, 1, connection)

            connection.close()


if __name__ == "__main__":
    unittest.main()
