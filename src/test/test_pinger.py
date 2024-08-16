import unittest
import sys, os
sys.path.append(os.path.abspath("./src"))

# from internet_sabotage import no_connection
import pinger

### NOTE: This test is not functioning as expected. internet_sabotage module isn't
### working therefore internet connection must be manually disabled before running

class TestPinger(unittest.TestCase):
    # @no_connection
    def test_pinger_handles_network_dropouts(self):
        pass
        # Test code goes here
        self.assertEqual(False, pinger.do_ping())

if __name__ == '__main__':
    unittest.main()