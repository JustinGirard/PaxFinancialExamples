
# Submitting an Order

In this example we show how to use the Pax Financial API to submit a market order in a simulation. We will place money in our account, submit an order, have the API check that it is possible to fill the order and fill it if possible, and view the filled order and our account holdings.      

## 1. Importing the PDK and Instantiating the API

We begin by importing the Pax Development Kit and instantiating the Pax Financial API. Upon executing the following cell you should see as output `PaxFinancialAPI v4 loaded!` (or something similar).


```python
import paxdk

import json
with open("../.config") as f:
    data = json.load(f)
api_key = data['api_key'] 
 
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)
```

    PaxFinancialAPI v4 loaded!


## 2. Generating an Experiment ID

Every experiment requires an experiment ID, so we generate a unique  but descriptive ID to use. 


```python
import uuid
eid = 'test_market_order-'+str(uuid.uuid1())
print(eid)
```

    test_market_order-ed987e8a-a5bb-11ea-b2d5-1b6781e48145


## 3. Loading Funds Into Our Account

We begin by putting some cash into the holdings associated with this experiment ID. We will load the account with USD10,000. 
The argument `'symbol'` specifies the ticker symbol for the security or currency in the transaction, which is 'USDT' for US dollars.  The `'quantity'` 10000 is the number of US dollars credited to our account in the transaction. The `'date'` is the simulation datetime at which the transaction occurs. We will have our transaction occurring at 9:00 am, April 1, 2020. 


```python
## 1  Put some cash into this EID
import datetime
transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'USDT',
                                'quantity': 10000,
                                'value': 10000,
                                'date':datetime.datetime(2020,4,1,9),
                                'unit_price': 1.0,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",
                                #'do_not_update_holdings':True,
                                'api_key':api_key},remote=True)
print(transdat)
assert 'transaction_id' in transdat.keys()
assert 'quantity' in transdat.keys()
assert 'symbol' in transdat.keys()

```

    {'transaction_id': 't-24458380-3305-4048-9def-b0e7bcaac27e', 'quantity': '10000', 'symbol': 'USDT'}


The `pq.submit_transaction()` API call returns a dictionary containing a `transaction_id` and the quantity and symbol of the transaction.

## 4. Submitting an Order

Now we will submit an order to buy BitCoin ('BTC').  The `from_symbol` is the currency our account is ('USDT' i.e. US dollars), the `to_symbol` is the security or currency we're buying. The `to_quantity` is the amount to buy. We will specify that we want to buy 0.1 BitCoin. We must specify the order type, which is either 'BUY' or 'SELL'.  In this case it is 'BUY'. The `purchase_date` is the simulation datetime (as opposed to the real datetime) at which the BUY order takes effect (i.e. you are requesting to buy after this time). We must also provide a `'limit_date'`, which is the simulation datetime at which the order will expire if it has not been filled. Here we choose a `'limit_date'` of 1 day after the order comes into effect.   


```python
from_symbol = 'USDT'
to_symbol = 'BTC'
to_quantity = 0.1
order_type = 'BUY'
purchase_date = datetime.datetime(2020,4,1,10)
limit_date = purchase_date + datetime.timedelta(days=1)
                
dat = pq.submit_single_market_order({'from_symbol':from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id':eid,
                            'type': order_type,
                            'purchase_date':purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            'limit_date': limit_date,
                            'symbol_discovery':'BINANCE',
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })    
print(dat)
assert 'order_id' in dat.keys()
assert 'experiment_id' in dat.keys()
assert dat['experiment_id'] == eid
assert 'status' in dat.keys()
assert dat['status'] == 'pending'
assert 'from_symbol' in dat.keys()
assert 'to_symbol' in dat.keys()
assert 'to_quantity' in dat.keys()
```

    {'from_symbol': 'USDT', 'order_id': 'ro-78e234bf-854e-4fae-9c85-95c77c9af1cd', 'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order-ed987e8a-a5bb-11ea-b2d5-1b6781e48145', 'type': 'BUY', 'purchase_date': datetime.datetime(2020, 4, 1, 10, 0), 'submitted_date': datetime.datetime(2020, 4, 1, 10, 0), 'tag': 'test submit', 'limit_price_top': None, 'limit_price_bottom': None, 'limit_date': datetime.datetime(2020, 4, 2, 10, 0), 'simulated_price': None, 'symbol_discovery': 'BINANCE', 'market_price': None, 'market_status': 'pending', 'status': 'pending', 'avg_fill_price': None, 'market_avg_fill_price': None, 'transaction_fee': None, 'transaction_ids': [], '_id': None}


The `pq.submit_single_order()` API call returns a dictionary with information about the order.  Note in particular the `'status'` field, which should have the value `'pending'`.  The initial status of an order upon submission is always `'pending'`. The order status will remain `'pending'` until we call `pq.manage_experiment()`, which is the task of the next code cell.

## 5. Filling the Order

The `pq.manage_experiment()` API call checks the orders for the `'experiment_id'` to see if there are any `'pending'` orders that can be filled at the `'current_date'` (which is actually a datetime) specified. If there are, it will fill the orders, making the appropriate transfers of assets and currency to and from the account. We are calling `pq.manage_experiment()` with `'current_date'` equal to one hour after our order came into effect i.e. 11:00 am April 1, 2020. 


```python
dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': datetime.datetime(2020,4,1,11),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,},remote=True)
print(dat)
assert dat is True
```

    True


A successful call to `'pq.manage_experiment()'` will return with the value `True`. 

## 6. Checking If the Order Was Filled

To see if the order was filled we call `pq.find_algorithm_single_orders()`: 


```python
q = {'experiment_id':eid}
dat = pq.find_algorithm_single_orders(q,remote=True)
print(dat)
assert 'order_id' in dat[0].keys()
assert 'experiment_id' in dat[0].keys()
assert dat[0]['experiment_id'] == eid
assert 'status' in dat[0].keys()
assert 'from_symbol' in dat[0].keys()
assert 'to_symbol' in dat[0].keys()
assert 'to_quantity' in dat[0].keys()
```

    [{'from_symbol': 'USDT', 'order_id': 'ro-78e234bf-854e-4fae-9c85-95c77c9af1cd', 'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order-ed987e8a-a5bb-11ea-b2d5-1b6781e48145', 'type': 'BUY', 'purchase_date': datetime.datetime(2020, 4, 1, 10, 0), 'submitted_date': datetime.datetime(2020, 4, 1, 10, 0), 'tag': 'test submit,Simulated Buy Fill', 'limit_price_top': None, 'limit_price_bottom': None, 'limit_date': datetime.datetime(2020, 4, 2, 10, 0), 'simulated_price': 6318.89, 'symbol_discovery': 'BINANCE', 'market_price': None, 'market_status': 'pending', 'status': 'filled', 'avg_fill_price': 6318.89, 'market_avg_fill_price': None, 'transaction_fee': None, 'transaction_ids': [], 'account_id': 'justingirard@justingirard.com'}]


`pq.find_algorithm_single_orders()` provides information about all orders submitted by the experiment. In this case there is only one order submitted so we obtain a one-element list. If the order has been filled the `'status'` will now be `'filled'` and the field `'avg_fill_price'` will state the price that was paid.

## 7. Viewing Our Account Holdings

Next we will call `'pq.get_approx_holdings'` to see what our experiment's holdings are.  The holdings are "approximate" in the sense that they are calculated by updating holdings in real-time as opposed to from a transaction history. 


```python
dat = pq.get_approx_holdings({'api_key':api_key,'experiment_id':eid},remote=True)
print(dat)
assert 'USDT' in dat.keys()
assert 'BTC' in dat.keys()
```

    {'USDT': 9367.47279211, 'BTC': 0.1}


In the dictionary returned from `pq.get_approx_holdings()` we can see the amounts of US dollars we hold, as well as the amount of BitCoin if the order placed above was successfully filled.


```python

```
