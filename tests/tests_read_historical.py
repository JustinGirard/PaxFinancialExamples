# This is a very minimal test. Its purpose is to establish that the paxdk can be loaded
# and instantiated, and that an endpoint can be called from it.


# We import the Pax Development Kit and instantiate the Pax Financial API:

import sys
sys.path.append("../paxdk")

import paxdk

with open("../.config") as f:
    data = json.load(f)
api_key = data['api_key']
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)

# We use the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar 
# exchange rate.

import datetime
import unittest

class TestReadHistorical(unittest.TestCase):
    def test_read_historical(self):
        bars = pq.get_historical_hour({'api_key':api_key,
                                'time_in':datetime.datetime(2020,4,1,10),
                                'time_end':datetime.datetime(2020,4,1,12),
                                'Ticker':'BTCUSDT',
                                                             },remote=True)
        self.assertTrue( 'HighPrice' in bars[0].keys() ) 
