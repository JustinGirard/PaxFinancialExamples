
# First Example of Use of the Pax Financial API: Reading Financial Data

In this example we  use the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar exchange rate, and we display the hour bars we obtain.

To begin we import the Pax Development Kit and instantiate the Pax Financial API. You must replace the API key in the example with your API key.


```python
import sys
sys.path.append("../paxdk")

import paxdk

# replace the API key in the line below with your API key
api_key = 'pkey-0123456789abcdef0123456789abcdef0123456789abcdef01234567' 
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)

```

    PaxFinancialAPI v4 loaded!


We use the `get_historical_hour` call of the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar exchange rate. We use a Pandas dataframe to display the hour bars we obtain.  Hour bars correspond to a one-hour period and contain the opening price, closing price, high price, and low price for that period.


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




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ClosePrice</th>
      <th>DateTime</th>
      <th>HighPrice</th>
      <th>LowPrice</th>
      <th>OpenPrice</th>
      <th>Ticker</th>
      <th>_id</th>
      <th>close</th>
      <th>date_time</th>
      <th>from_symbol</th>
      <th>high</th>
      <th>low</th>
      <th>open</th>
      <th>requested_date</th>
      <th>time</th>
      <th>to_symbol</th>
      <th>volumefrom</th>
      <th>volumeto</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>BTC</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>2020-04-03T12:35:19.395000</td>
      <td>1585735200</td>
      <td>USDT</td>
      <td>19079.12</td>
      <td>1.202464e+08</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>BTC</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>2020-04-03T12:35:42.676000</td>
      <td>1585735200</td>
      <td>USDT</td>
      <td>19079.12</td>
      <td>1.202464e+08</td>
    </tr>
    <tr>
      <th>2</th>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6295.03</td>
      <td>2020-04-01 10:00:00</td>
      <td>BTC</td>
      <td>6318.89</td>
      <td>6288.02</td>
      <td>6298.74</td>
      <td>2020-04-03T14:02:44.635000</td>
      <td>1585735200</td>
      <td>USDT</td>
      <td>19079.12</td>
      <td>1.202464e+08</td>
    </tr>
    <tr>
      <th>3</th>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>BTC</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>2020-04-03T12:35:19.395000</td>
      <td>1585738800</td>
      <td>USDT</td>
      <td>20212.56</td>
      <td>1.271062e+08</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>BTC</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>2020-04-03T12:35:42.676000</td>
      <td>1585738800</td>
      <td>USDT</td>
      <td>20212.56</td>
      <td>1.271062e+08</td>
    </tr>
    <tr>
      <th>5</th>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6294.25</td>
      <td>2020-04-01 11:00:00</td>
      <td>BTC</td>
      <td>6301.76</td>
      <td>6271.20</td>
      <td>6295.03</td>
      <td>2020-04-03T14:02:44.635000</td>
      <td>1585738800</td>
      <td>USDT</td>
      <td>20212.56</td>
      <td>1.271062e+08</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>BTC</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>2020-04-03T12:35:19.395000</td>
      <td>1585742400</td>
      <td>USDT</td>
      <td>46717.66</td>
      <td>2.918826e+08</td>
    </tr>
    <tr>
      <th>7</th>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>BTC</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>2020-04-03T12:35:42.676000</td>
      <td>1585742400</td>
      <td>USDT</td>
      <td>46717.66</td>
      <td>2.918826e+08</td>
    </tr>
    <tr>
      <th>8</th>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>BTCUSDT</td>
      <td>None</td>
      <td>6217.51</td>
      <td>2020-04-01 12:00:00</td>
      <td>BTC</td>
      <td>6332.16</td>
      <td>6215.66</td>
      <td>6294.25</td>
      <td>2020-04-03T14:02:44.635000</td>
      <td>1585742400</td>
      <td>USDT</td>
      <td>46717.66</td>
      <td>2.918826e+08</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
