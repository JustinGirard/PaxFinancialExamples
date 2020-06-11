# `submit_single_market_order`

## Description

This endpoint creates a market order that is either simulated or live on the market, or both.

### Arguments

**api_key :* str***
 
a valid API key
 
**from_symbol :* str***

the ticker symbol for the currency of the account

**to_symbol :* str***

the ticker symbol for the security being bought or sold
  
**to_quantity :* number*** 

units of the security to buy or sell
  
**experiment_id :* str*** 

the experiment ID under which the order is to be submitted

**type :* str***

the transaction type. Must be 'BUY' or 'SELL'.

**purchase_date :* datetime*** 

the datetime at which the order comes into effect. The
 security will not be bought or sold before this datetime.

**limit_price_bottom :* number*** or ***Nonetype***

 the bottom price limit. The security will not be bought or
sold below this price.  May be `None`. Optional.
  
**limit_price_top :* number*** or ***Nonetype***

the top price limit. The security will not be bought or sold
 above this price. May be `None`. Optional.
 
**limit_date :* datetime***  or ***Nonetype***

the expiry datetime for the order. The security will not be bought or sold after this datetime. May be `None`. Optional.
  
**symbol_discovery :* str***

symbol discovery to use for the order.  'BINANCE' for
 currency and crypto, 'IB' for stocks.


## Simple Example

    dat = pq.submit_single_market_order({'from_symbol': 'USDT',
                                'to_symbol': 'BTC',
                                'to_quantity': 0.1,
                                'experiment_id': 'test_market_order',
                                'type': 'BUY',
                                'purchase_date': datetime.datetime.utcnow(),
                                'tag':"test submit",
                                'symbol_discovery': 'BINANCE'
                                  })
    print(dat)

## Simple Example Output

    {'from_symbol': 'USDT', 'order_id': 'ro-2a979be7-7628-4a22-b32a-67ffe41035e2', 
    'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order', 
    'type': 'BUY', 'purchase_date': '2020-06-10T19:01:44.207178', 
    'submitted_date': '2020-06-10T19:01:44.207178', 'tag': 'test submit', 
    'limit_price_top': None, 'limit_price_bottom': None, 'limit_date': '2020-06-10T20:01:45.117027', 
    'simulated_price': None, 'symbol_discovery': 'BINANCE', 'market_price': None, 
    'market_status': 'pending', 'status': 'pending', 'avg_fill_price': None, 
    'market_avg_fill_price': None, 'transaction_fee': None, 
    'transaction_ids': [], '_id': None}

## Failure Examples

    # submit without experiment_id
    # an experiment id is required
        
    dat = pq.submit_single_market_order({'from_symbol': 'USDT',
                                'to_symbol': 'BTC',
                                'to_quantity': 0.1,
                                #'experiment_id': 'test_market_order',
                                'type': 'BUY',
                                'purchase_date': datetime.datetime.utcnow(),
                                'tag':"test submit",
                                'symbol_discovery': 'BINANCE'
                                  })
    print(dat)

## Failure Examples Output

    {'error': 'No Target Process'}

## Three Examples

    # 1 with a limit date 
    
    dat = pq.submit_single_market_order({'from_symbol':'USDT',
                                'to_symbol': 'BTC',
                                'to_quantity': 0.1,
                                'experiment_id':'test_market_order',
                                'type': 'BUY',
                                'purchase_date': ,datetime.datetime.utcnow()
                                'tag':"test submit",             
                                'limit_date': datetime.datetime.utcnow()+datetime.timedelta(days=1),
                                'symbol_discovery':'BINANCE',                 
                                  })    
    print(dat)
    
    
     
      
    # 2 limit date as well as top and bottom price limits
    
    dat = pq.submit_single_market_order({  'experiment_id': 'test_market_order',
                   'from_symbol':'USDT',
                   'to_symbol': 'BTC',
                   'to_quantity': 0.1,
                   'type': 'BUY',
                   'purchase_date': datetime.datetime(2020,4,1,10),
                   'tag':"test submit",
                   'limit_price_top': 6310.0,
                   'limit_price_bottom': 6295.0,
                   'limit_date': datetime.datetime(2020,4,1,12),
                   'symbol_discovery':'BINANCE',                 
                }
                , remote=True)  
    print(dat)
    
    
    
    # 3 a SELL with a limit date and price limits
    
    dat = pq.submit_single_market_order({  'experiment_id': "test_market_order",
                   'from_symbol':'USDT',
                   'to_symbol': 'BTC',
                   'to_quantity': 0.1,
                   'type': 'SELL',
                   'purchase_date': datetime.datetime(2020,4,1,10),
                   'tag':"test submit",
                   'limit_price_top': 6310.0,
                   'limit_price_bottom': 6295.0,
                   'limit_date': datetime.datetime(2020,4,1,12),
                   'symbol_discovery':'BINANCE',                 
                }
                , remote=True)  
    print(dat)

## Three Examples Output

    {'from_symbol': 'USDT', 'order_id': 'ro-712809a8-9db5-4f66-a0b5-8dcad5d6fcc9', 
    'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order', 
    'type': 'BUY', 'purchase_date': '2020-06-10T19:10:30.948144', 
    'submitted_date': '2020-06-10T19:10:30.948144', 'tag': 'test submit', 
    'limit_price_top': None, 'limit_price_bottom': None,'limit_date': '2020-06-11T19:10:30.948144', 
    'simulated_price': None, 'symbol_discovery': 'BINANCE', 'market_price': None, 
    'market_status': 'pending', 'status': 'pending', 'avg_fill_price': None, 
    'market_avg_fill_price': None, 'transaction_fee': None, 
    'transaction_ids': [], '_id': None}
    
    
    {'from_symbol': 'USDT', 'order_id': 'ro-ec067a7b-c27b-4052-b43a-3413b4d36836', 
    'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order', 
    'type': 'BUY', 'purchase_date': datetime.datetime(2020, 4, 1, 10, 0),
    'submitted_date': datetime.datetime(2020, 4, 1, 10, 0), 'tag': 'test submit', 
    'limit_price_top': 6310.0, 'limit_price_bottom': 6295.0, 
    'limit_date': datetime.datetime(2020, 4, 1, 12, 0), 'simulated_price': None, 
    'symbol_discovery': 'BINANCE', 'market_price': None, 'market_status': 'pending', 
    'status': 'pending', 'avg_fill_price': None, 'market_avg_fill_price': None, 
    'transaction_fee': None, 'transaction_ids': [], 
    '_id': None}
    
    
    {'from_symbol': 'USDT', 'order_id': 'ro-09311000-8d27-4f08-a6a4-079ea56f09f5', 
    'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order', 
    'type': 'SELL', 'purchase_date': datetime.datetime(2020, 4, 1, 10, 0),
     'submitted_date': datetime.datetime(2020, 4, 1, 10, 0), 'tag': 'test submit', 
    'limit_price_top': 6310.0, 'limit_price_bottom': 6295.0,
    'limit_date': datetime.datetime(2020, 4, 1, 12, 0), 'simulated_price': None, 
    'symbol_discovery': 'BINANCE', 'market_price': None, 'market_status': 'pending', 
    'status': 'pending', 'avg_fill_price': None, 'market_avg_fill_price': None, 
    'transaction_fee': None, 'transaction_ids': [], '_id': None}

