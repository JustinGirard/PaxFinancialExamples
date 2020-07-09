# PaxFinancialExamples

Examples of the use of the Pax Financial API.

The Pax Financial API is a framework for handling financial data and running financial simulations.   

This repository contains examples that illustrate the use of the Pax Financial API.

The Pax Financial API is of interest to computer science enthusiasts and people interested in visualization of financial data.

## Setup Instructions

    clone https://github.com/chemming/PaxFinancialExamples.git
    cd PaxFinancialExamples
    python setup.py

## A Simple Example of the Use of the API

examples/FirstExample.py is a simple example illustrating the importing of the Pax Development Kit, the instantiation of the Pax Financial API, and the calling of an API endpoint to retrieve historical price data for a currency exchange rate.

    # We import the Pax Development Kit and instantiate the Pax Financial API:

    import sys
    sys.path.append("../paxdk")

    import paxdk

    with open("../.config") as f:
        data = json.load(f)
    api_key = data['api_key'] 
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
