import unittest
import sys, os
sys.path.append(os.path.abspath(".."))

from internet_sabotage import no_connection

from src import pinger

class TestPinger(unittest.TestCase):
    @no_connection
    def testPingerHandlesNetworkDropouts(self):
        # Test code goes here
        pinger.ping_and_record()

if __name__ == '__main__':
    unittest.main()