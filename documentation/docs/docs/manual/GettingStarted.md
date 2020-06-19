
# Getting Started

This example will get you started with downloading and setting up the Pax Financial Examples package, show you how to sign up with Pax Financial and find your API key, and then guide you through a simple example in which we use the Pax Financial API to download some historical financial price data.

## Downloading and Setting Up the Pax Financial Examples Software Package

1. Clone the git repository and execute the setup.py script.

        clone https://github.com/JustinGirard/PaxFinancialExamples.git
        cd PaxFinancialExamples
        python3 setup.py
        
2. Add the `PaxFinancialExamples/paxdk` directory to your system's PYTHONPATH, by running from a terminal
        
        export PYTHONPATH = $PYTHONPATH:/<path>/PaxFinancialExamples/paxdk

## Signing Up With Pax Financial

1. In a web browser, navigate to <https://g46w1ege85.execute-api.us-west-2.amazonaws.com/alpha/dev/paxfinancial/console/get> . 
2. Sign in with Google or your e-mail, according to the instructions.

## Finding your API key

Once you have signed up and signed in, you are ready to locate your API key.

1. In the top left corner of the screen that appears when you sign in, there is a hamburger icon (three stacked horizontal lines). Click this icon. A panel should slide out from the left side of the screen. You will see your API key.

2. Copy the API key. Open the file `PaxFinancialExamples/.config` with an editor and replace the API key in the file with your API key. 

Once you have your API key entered into the `.config` file, you are ready to execute the first example of using the Pax Financial API.

## A First Example: Reading Financial Data

In our first example of the use of the Pax Financial API we will read some historical price data and display it. This example is a Jupyter Notebook (as are all the examples) which is located at `PaxFinancialExamples/examples/ReadingFinancialData.ipynb`. In the first code cell, replace the API key with your own API key. After that you can run the notebook by using the "run" button to execute the code cells in the order they appear.

We import the Pax Development Kit and instantiate the Pax Financial API:


```python
import paxdk

import json
with open("../.config") as f:
    data = json.load(f)
api_key = data['api_key']
    
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)
```

We use the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar exchange rate, and we display the hour bars we obtain. An hour bar corresponds to a one-hour period and contains the opening price, closing price, high price, and low price for that period.


```python
import pandas as pd
import datetime

bars = pq.get_historical_hour({'api_key':api_key,
                                'time_in':datetime.datetime(2020,4,1,10),
                                'time_end':datetime.datetime(2020,4,1,12),
                                'Ticker':'BTCUSDT',
                                                             },remote=True)
df=pd.DataFrame(bars)
df
```

Executing the code cells should display a Pandas dataframe of the hour bars data.