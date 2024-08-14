import unittest

from db_connector import create_connection

class TestFetchedData(unittest.TestCase):
    def testDontGetDataOutsideTimeframe(self):
        connection = create_connection("src/test/test_network_history.db") # should create db if not already there

        if connection:
            cursor = connection.cursor()

            result = cursor.execute("CREATE TABLE  network_history (id INTEGER PRIMARY KEY, datetime TEXT, average_ping REAL, packet_loss REAL, network_down BOOLEAN DEFAULT FALSE)")

            cursor.execute("INSERT INTO network_history VALUES(NULL, ?, 100, 0.3, 1)")

            connection.commit()
            connection.close()
