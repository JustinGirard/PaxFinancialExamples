
# Reading Financial Data

In this example we  use the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar exchange rate, and we display the hour bars we obtain.

To begin we import the Pax Development Kit and instantiate the Pax Financial API. You must replace the API key in the example with your API key.


```python
import paxdk

import json
with open("../.config") as f:
    data = json.load(f)
api_key = data['api_key']   

pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key) 
```

    PaxFinancialAPI v4 loaded!


We use the `get_historical_hour` call of the Pax Financial API to read some historical hourly price data about the Bitcoin/US dollar exchange rate. We use a Pandas dataframe to display the hour bars we obtain.  Hour bars correspond to a one-hour period and contain the opening price, closing price, high price, and low price for that period.


```python
import pandas as pd
import datetime

bars = pq.get_historical_hour({'api_key':api_key,
                                'time_in':datetime.datetime(2020,4,1,10),
                                'time_end':datetime.datetime(2020,4,2,10),
                                'Ticker':'BTCUSDT',
                              },remote=True)
df=pd.DataFrame(bars)
df[['DateTime','Ticker','OpenPrice','ClosePrice','HighPrice','LowPrice']]
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
      <th>DateTime</th>
      <th>Ticker</th>
      <th>OpenPrice</th>
      <th>ClosePrice</th>
      <th>HighPrice</th>
      <th>LowPrice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2020-04-01 10:00:00</td>
      <td>BTCUSDT</td>
      <td>6298.74</td>
      <td>6295.03</td>
      <td>6318.89</td>
      <td>6288.02</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2020-04-01 11:00:00</td>
      <td>BTCUSDT</td>
      <td>6295.03</td>
      <td>6294.25</td>
      <td>6301.76</td>
      <td>6271.20</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2020-04-01 12:00:00</td>
      <td>BTCUSDT</td>
      <td>6294.25</td>
      <td>6217.51</td>
      <td>6332.16</td>
      <td>6215.66</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2020-04-01 13:00:00</td>
      <td>BTCUSDT</td>
      <td>6217.51</td>
      <td>6207.82</td>
      <td>6237.52</td>
      <td>6184.44</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2020-04-01 14:00:00</td>
      <td>BTCUSDT</td>
      <td>6207.82</td>
      <td>6248.66</td>
      <td>6259.88</td>
      <td>6200.55</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2020-04-01 15:00:00</td>
      <td>BTCUSDT</td>
      <td>6248.66</td>
      <td>6230.79</td>
      <td>6257.52</td>
      <td>6223.01</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2020-04-01 16:00:00</td>
      <td>BTCUSDT</td>
      <td>6230.79</td>
      <td>6186.38</td>
      <td>6232.66</td>
      <td>6153.80</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2020-04-01 17:00:00</td>
      <td>BTCUSDT</td>
      <td>6186.38</td>
      <td>6196.06</td>
      <td>6211.07</td>
      <td>6170.05</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2020-04-01 18:00:00</td>
      <td>BTCUSDT</td>
      <td>6196.06</td>
      <td>6187.99</td>
      <td>6216.32</td>
      <td>6183.59</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2020-04-01 19:00:00</td>
      <td>BTCUSDT</td>
      <td>6187.99</td>
      <td>6205.43</td>
      <td>6211.38</td>
      <td>6166.86</td>
    </tr>
    <tr>
      <th>10</th>
      <td>2020-04-01 20:00:00</td>
      <td>BTCUSDT</td>
      <td>6205.43</td>
      <td>6336.67</td>
      <td>6365.32</td>
      <td>6193.98</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2020-04-01 21:00:00</td>
      <td>BTCUSDT</td>
      <td>6336.67</td>
      <td>6352.28</td>
      <td>6394.89</td>
      <td>6336.55</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2020-04-01 22:00:00</td>
      <td>BTCUSDT</td>
      <td>6352.28</td>
      <td>6519.82</td>
      <td>6576.95</td>
      <td>6352.16</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2020-04-01 23:00:00</td>
      <td>BTCUSDT</td>
      <td>6519.82</td>
      <td>6633.43</td>
      <td>6665.77</td>
      <td>6500.76</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2020-04-02 00:00:00</td>
      <td>BTCUSDT</td>
      <td>6633.43</td>
      <td>6611.25</td>
      <td>6723.47</td>
      <td>6587.76</td>
    </tr>
    <tr>
      <th>15</th>
      <td>2020-04-02 01:00:00</td>
      <td>BTCUSDT</td>
      <td>6611.25</td>
      <td>6566.67</td>
      <td>6636.58</td>
      <td>6565.87</td>
    </tr>
    <tr>
      <th>16</th>
      <td>2020-04-02 02:00:00</td>
      <td>BTCUSDT</td>
      <td>6566.67</td>
      <td>6604.55</td>
      <td>6615.40</td>
      <td>6565.85</td>
    </tr>
    <tr>
      <th>17</th>
      <td>2020-04-02 03:00:00</td>
      <td>BTCUSDT</td>
      <td>6604.55</td>
      <td>6605.23</td>
      <td>6613.51</td>
      <td>6579.68</td>
    </tr>
    <tr>
      <th>18</th>
      <td>2020-04-02 04:00:00</td>
      <td>BTCUSDT</td>
      <td>6605.23</td>
      <td>6596.21</td>
      <td>6627.00</td>
      <td>6588.75</td>
    </tr>
    <tr>
      <th>19</th>
      <td>2020-04-02 05:00:00</td>
      <td>BTCUSDT</td>
      <td>6596.21</td>
      <td>6604.09</td>
      <td>6604.89</td>
      <td>6566.94</td>
    </tr>
    <tr>
      <th>20</th>
      <td>2020-04-02 06:00:00</td>
      <td>BTCUSDT</td>
      <td>6604.09</td>
      <td>6638.63</td>
      <td>6642.13</td>
      <td>6590.18</td>
    </tr>
    <tr>
      <th>21</th>
      <td>2020-04-02 07:00:00</td>
      <td>BTCUSDT</td>
      <td>6638.63</td>
      <td>6644.80</td>
      <td>6673.98</td>
      <td>6613.71</td>
    </tr>
    <tr>
      <th>22</th>
      <td>2020-04-02 08:00:00</td>
      <td>BTCUSDT</td>
      <td>6644.80</td>
      <td>6648.31</td>
      <td>6665.18</td>
      <td>6611.15</td>
    </tr>
    <tr>
      <th>23</th>
      <td>2020-04-02 09:00:00</td>
      <td>BTCUSDT</td>
      <td>6648.31</td>
      <td>6640.26</td>
      <td>6656.08</td>
      <td>6624.23</td>
    </tr>
    <tr>
      <th>24</th>
      <td>2020-04-02 10:00:00</td>
      <td>BTCUSDT</td>
      <td>6640.26</td>
      <td>6646.44</td>
      <td>6693.88</td>
      <td>6622.85</td>
    </tr>
  </tbody>
</table>
</div>



With the price data in a dataframe, we can easily plot the data with Matplotlib. For example, we can plot the high and low prices against time:


```python
import matplotlib.pyplot as plt
plt.plot(df['DateTime'],df['HighPrice'])
plt.plot(df['DateTime'],df['LowPrice'])
plt.show()
```


![png](output_7_0.png)



```python

```
