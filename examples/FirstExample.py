# We import the Pax Development Kit and instantiate the Pax Financial API:

import sys
sys.path.append("../paxdk")

import paxdk

api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)

# We use the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar 
# exchange rate, and we display the hour bars we obtain.

import pandas as pd
import datetime

bars = pq.get_historical_hour({'api_key':api_key,
                                'time_in':datetime.datetime(2020,4,1,10),
                                'time_end':datetime.datetime(2020,4,1,12),
                                'Ticker':'BTCUSDT',
                                                             },remote=True)
print(bars)
