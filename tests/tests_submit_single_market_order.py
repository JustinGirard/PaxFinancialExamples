import sys
sys.path.append("../")
sys.path.append("../../")

import paxdk
import importlib
importlib.reload(paxdk)
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
pq = paxdk.PaxFinancialAPI(url_version='dev')

api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
import datetime,time
import unittest
import uuid

class TestSubmitSingleMarketOrder(unittest.TestCase):
                                                         
    def test_order_submission(self):
  
        from_symbol = 'USDT'
        to_symbol = 'BTC'
        to_quantity = 0.1
        eid = 'test_market_order'
        order_type = 'BUY'
        purchase_date = datetime.datetime.utcnow()
        
        submitted_date_approx = datetime.datetime.utcnow()
        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': order_type,
                            'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })
      
        self.assertTrue('status' in dat.keys(),"response should contain 'status' field")
        self.assertEqual(dat['status'],'pending',"status of submitted order should be 'pending'")
        self.assertTrue('from_symbol' in dat.keys(), "response should contain 'from_symbol' field")
        self.assertEqual(dat['from_symbol'],from_symbol, "dat['from_symbol'] should be "+str(from_symbol))
        self.assertTrue('order_id' in dat.keys(), "response should contain 'order_id' field")
        self.assertTrue('to_symbol' in dat.keys(), "response should contain 'to_symbol' field")
        self.assertEqual(dat['to_symbol'],to_symbol, "dat['to_symbol'] should be "+str(to_symbol))
        self.assertTrue('to_quantity' in dat.keys(), "response should contain 'to_quantity' field")
        self.assertEqual(dat['to_quantity'], to_quantity, "dat['to_quantity'] should be "+str(to_quantity))
        self.assertTrue('experiment_id' in dat.keys(), "response should contain 'experiment_id' field")
        self.assertEqual(dat['experiment_id'],eid,"dat['experiment_id'] should be "+str(eid))
        self.assertTrue('type' in dat.keys(),"response should contain 'type' field")
        self.assertEqual(dat['type'], order_type, "dat['type'] should be "+str(order_type))
        self.assertTrue('purchase_date' in dat.keys(), "response should contain 'purchase_date' field")
        self.assertEqual(dat['purchase_date'],purchase_date.isoformat(),"dat['purchase_date'] should be "+str(purchase_date.isoformat()))
        self.assertTrue('submitted_date' in dat.keys(), "response should contain 'submitted_date' field")
        
        dt = submitted_date_approx - datetime.datetime.fromisoformat(dat['submitted_date'])
        dt = abs(dt)
        self.assertTrue( dt <= datetime.timedelta(hours=1), 
                         "dat['submitted_date'] should be within 1 hour of " + submitted_date_approx.isoformat() ) 
        
        self.assertTrue('tag' in dat.keys(), "response should contain 'tag' field")
        self.assertTrue('limit_price_top' in dat.keys(), "response should contain 'limit_price_top' field")
        self.assertTrue('limit_price_bottom' in dat.keys(), "response should contain 'limit_price_bottom' field")
        self.assertTrue('limit_date' in dat.keys(), "response should contain 'limit_date' field")
        self.assertTrue('simulated_price' in dat.keys(), "response should contain 'simulated_price' field")
        self.assertTrue('symbol_discovery' in dat.keys(), "response should contain 'symbol_discovery' field")
        self.assertTrue('market_price' in dat.keys(), "response should contain 'market_price' field")
        self.assertTrue('market_status' in dat.keys(), "response should contain 'market_status' field")
        self.assertTrue('avg_fill_price' in dat.keys(), "response should contain 'avg_fill_price' field")
        self.assertTrue('market_avg_fill_price' in dat.keys(), "response should contain 'market_avg_fill_price' field")
        self.assertTrue('transaction_fee' in dat.keys(), "response should contain 'transaction_fee' field")
        self.assertTrue('transaction_ids' in dat.keys(), "respsonse should contain 'transaction_ids' field")
         
        
        # submit without experiment_id
    
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            #'experiment_id': eid,
                            'type': order_type,
                            'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })
                
        self.assertTrue('error' in dat.keys(), "should be 'error' field in response")
        self.assertEqual( dat['error'], "No Target Process", "Error message should be 'No Target Process'")
    
        # submit without purchase_date
        # this is the minimal order (except possibly for the 'tag' field) that can be valid
        submitted_date_approx = datetime.datetime.utcnow()        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': order_type,
                            #'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })    
        self.assertTrue( 'purchase_date' in dat.keys(), "response should contain 'purchase_date' field" ) 
        dt = submitted_date_approx - datetime.datetime.fromisoformat(dat['purchase_date'])
        dt = abs(dt)
        self.assertTrue( dt <= datetime.timedelta(hours=1), 
                         "dat['purchase_date'] should be within 1 hour of " + submitted_date_approx.isoformat() )         
        
        # submit without to_quantity
        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            #'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': order_type,
                            #'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })            
        
        self.assertTrue('error' in dat.keys(), "response should contain 'error' field")
        
        # submit without to_symbol
        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            #'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': order_type,
                            #'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })            
        
        self.assertTrue('error' in dat.keys(), "response should contain 'error' field")
        
        # submit without from_symbol
        
        dat = pq.submit_single_market_order({#'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': order_type,
                            #'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })
        
        self.assertTrue('error' in dat.keys(), "response should contain 'error' field")
        
        # submit without order type
        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            #'type': order_type,
                            'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })
        
        self.assertTrue('error' in dat.keys(), "response should contain 'error' field")
    
        # submit with invalid order type
        
        dat = pq.submit_single_market_order({'from_symbol': from_symbol,
                            'to_symbol': to_symbol,
                            'to_quantity': to_quantity,
                            'experiment_id': eid,
                            'type': 'market_order',
                            'purchase_date': purchase_date,
                            'tag':"test submit",
                            #'limit_value': None,
                            #'limit_date': self.context['current_date'] + datetime.timedelta(days=1),
                            #'market_price':None,
                            #'avg_fill_price':None,
                            #'market_status':None,
                            #'status':'simulated',
                            #'transaction_fee':min([proceeds*0.005,0.01*proceeds])*2,
                            #'transaction_ids':transaction_ids}
                              })

        self.assertTrue('error' in dat.keys(), "response should contain 'error' field")        
    
    def test_order_filling(self):
        
        # an order for one day ago
        
        eid = 'test_market_order-'+str(uuid.uuid1())
        
        ## 1  Put some cash into this EID
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'USDT',
                                'quantity': 1000000,
                                'value': 1000000,
                                'date':datetime.datetime.utcnow()-datetime.timedelta(days=1),
                                'unit_price': 1.0,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",
                                #'do_not_update_holdings':True,
                                'api_key':api_key},remote=True)
        print(transdat )    
        self.assertTrue('transaction_id' in transdat.keys())
        
        from_symbol = 'USDT'
        to_symbol = 'BTC'
        to_quantity = 0.1
        order_type = 'BUY'
        purchase_date = datetime.datetime.utcnow()-datetime.timedelta(days=1)
        #purchase_date = datetime.datetime.fromisoformat('2020-04-01T10:00:00')
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
        self.assertEqual(dat['status'],'pending',"order status after submission should be 'pending'")
        self.assertEqual(dat['limit_date'],limit_date.isoformat(),"limit_date should be "+limit_date.isoformat())
        
         
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date':datetime.datetime.utcnow()-datetime.timedelta(days=1),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,},remote=True)
        print(dat)
        self.assertTrue(dat is True)
        
        q = {'experiment_id':eid}
        dat = pq.find_algorithm_single_orders(q,remote=True)
        print(dat[0])
        self.assertEqual(dat[0]['status'],'filled')
 
 
        # an order with purchase_date = now
        
        eid = 'test_market_order-'+str(uuid.uuid1())
        
        ## 1  Put some cash into this EID
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'USDT',
                                'quantity': 1000000,
                                'value': 1000000,
                                'date':datetime.datetime.utcnow(),
                                'unit_price': 1.0,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",
                                #'do_not_update_holdings':True,
                                'api_key':api_key},remote=True)
        print(transdat ) 
        self.assertTrue('transaction_id' in transdat.keys())
        
        from_symbol = 'USDT'
        to_symbol = 'BTC'
        to_quantity = 0.1
        order_type = 'BUY'
        purchase_date = datetime.datetime.utcnow()
        #purchase_date = datetime.datetime.fromisoformat('2020-04-01T10:00:00')
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
        self.assertEqual(dat['status'],'pending',"order status after submission should be 'pending'")
        self.assertEqual(dat['limit_date'],limit_date.isoformat(),"limit_date should be "+limit_date.isoformat())
        
         
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date':datetime.datetime.utcnow(),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,},remote=True)
        print(dat)        
        self.assertTrue(dat is True)
        
        q = {'experiment_id':eid}
        dat = pq.find_algorithm_single_orders(q,remote=True)
        print(dat)
        self.assertEqual(dat[0]['status'],'filled')    

    def standardized_tst(self,tst):
        q = tst['order'].copy()
        expected_status = tst['expected_status']
       
        eid = 'test_market_order-'+str(uuid.uuid1()) 
    
        assert q['type'] in ['BUY','SELL'], "order type must be 'BUY' or 'SELL'"    

        account_currency = 'USDT'
        
        if q['to_symbol']=='AAPL':
            account_currency = 'CAD'
            limit_high = 200
            limit_low = 5
            
            for limit_price in ['limit_price_top','limit_price_bottom']:     
                if limit_price in q.keys():
                    if q[limit_price] == 10000:
                        q[limit_price] = limit_high
                    elif q[limit_price] == 5000:
                        q[limit_price] = limit_low
                    
        if q['type'] == 'BUY':                       
                               
            transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': q['from_symbol'],
                                'quantity': 1000000,
                                'value': 1000000,
                                'date': q['purchase_date'],
                                'unit_price': 1.0,
                                'account_currency': account_currency,
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",                                
                                'api_key':api_key},remote=True)
                               
        elif q['type'] == 'SELL': 
                               
            transdat = pq.submit_transaction({  
                                'experiment_id': eid,
                                'symbol': q['to_symbol'],
                                'quantity': 2.0*q['to_quantity'],
                                'value': 5000*2.0*q['to_quantity'],
                                'date': q['purchase_date'],
                                'unit_price': 5000,
                                'account_currency': account_currency,
                                'type': 'algorithm',
                                'note': "Initial Security Deposit",                                
                                'api_key':api_key},remote=True) 
                               
        assert 'transaction_id' in transdat.keys(), "response from pq.submit_transaction() is " + repr(transdat) 
                
        q['experiment_id'] = eid  
        
        #print(q)
        
        dat = pq.submit_single_market_order(q, remote=True)  
        assert dat['status']=='pending', "response from pq.submit_single_market_order is " + repr(dat)
        
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': q['purchase_date']+datetime.timedelta(hours=1),
                                    'base_symbol':q['from_symbol'],
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,
                                                      },remote=True)
       
        assert dat is True, "response from pq.manage_experiment() is " +repr(dat)
    
        dat = pq.find_algorithm_single_orders({'experiment_id':eid},remote=True)
        if dat[0]['status'] != expected_status:                       
            print(dat)
        assert dat[0]['status']==expected_status, "response from pq.find_algorithm_single_orders() is " + repr(dat)                                                      
                  
            
    def test_attempted_status_updates(self):
        securities_list = [ { 'order' : { 'from_symbol':'USDT',
                                   'to_symbol': 'BTC',
                                   'to_quantity': 0.1, 
                                   'symbol_discovery':'BINANCE',
                                   #'limit_price_top': 10000,
                                   #'limit_price_bottom': 5000,
                                       
                                   'tag':"test submit", },  
                       }, 
                       { 'order' : { 'from_symbol':'CAD',
                                   'to_symbol': 'AAPL',
                                   'to_quantity': 1.0, 
                                   'symbol_discovery':'IB',
                                  #'limit_price_top': 10000,
                                   #'limit_price_bottom': 5000,
                                       
                                   'tag':"test submit", },  
                       },         
                     ]
               
        test_list = [ 
                         #1) no limits
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'filled' 
                      },
            
                         #2) no limits, times out
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_date': datetime.datetime(2020,4,1,10,30),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'cancelled' 
                      },            
            
                         #3) large limit_price_top
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                   'limit_price_top': 10000,
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'filled' 
                      }, 
                          # limit_price_top too small to fill
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_price_top': 5000,
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                         'expected_status':  'pending' 
                      },             
                          # limit_price_top too small to fill, times out
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_price_top': 5000,
                                    'limit_date': datetime.datetime(2020,4,1,10,30),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'cancelled' 
                      },  
                          # low limit_price_bottom            
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_price_bottom': 5000,
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'filled' 
                      }, 
                          # limit_price_bottom too high to fill
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_price_bottom': 10000,
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'pending' 
                      },  
                           # limit_price_bottom too high to fill, times out
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag':"test submit",
                                    'limit_price_bottom': 10000,
                                    'limit_date': datetime.datetime(2020,4,1,10,30),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'cancelled' 
                      },
            
                         # high top limit, low bottom limit
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag': "test submit",
                                    'limit_price_top': 10000,
                                    'limit_price_bottom': 5000,
                                    'limit_date': datetime.datetime(2020,4,1,12),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'filled' 
                      }, 
            
                         # high top limit, low bottom limit, times out
                      { 'order': {  'from_symbol':'USDT',
                                    'to_symbol': 'BTC',
                                    'to_quantity': 0.1,
                                    'type': 'BUY',
                                    'purchase_date': datetime.datetime(2020,4,1,10),
                                    'tag': "test submit",
                                    'limit_price_top': 10000,
                                    'limit_price_bottom': 5000,
                                    'limit_date': datetime.datetime(2020,4,1,10,30),
                                    'symbol_discovery':'BINANCE',                 
                                 } , 
                          'expected_status':  'cancelled' 
                      }, 
                    ]
        failures = 0
        for securities in securities_list:                                                          
            for order_type in ['BUY','SELL']:                                              
                for tst in test_list:
                    tst1=tst.copy()
                    #print(tst1)
                    tst1['order'].update(securities['order'])
                    tst1['order']['type'] = order_type 
                    #print(tst1)
                    #if 'limit_price_top' in tst1['order'].keys():
                    #    tst1['order']['limit_price_top'] = order['limits'][tst1['order']['limit_price_top']]
                    
                    #print(tst1)
                    try: 
                        self.standardized_tst(tst1)                                          
                    except Exception as e:
                        failures = failures+1
                        print("FAILURE")
                        print("=======")
                        print(repr(tst1))
                        print(repr(e))
        self.assertEqual(failures,0,"some of the tests have failed")
        
        
    def test_price_limits(self): 
        
        bars = pq.get_historical_hour({'api_key':api_key,
                                'time_in':datetime.datetime(2020,4,1,10),
                                'time_end':datetime.datetime(2020,4,1,10,45),
                                'Ticker':'BTCUSDT',
                                                             },remote=True)
                
        HighPrice = bars[0]['HighPrice']
        LowPrice = bars[0]['LowPrice']
        
        # 1
        
        eid = str(uuid.uuid1())
        
        limit_price_top = 6400.0
        limit_price_bottom = 6295.0
        order_type = 'BUY'
        
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'USDT',
                                'quantity': 1000000,
                                'value': 1000000,
                                'date': datetime.datetime(2020,4,1,10),
                                'unit_price': 1.0,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",                                
                                'api_key':api_key},remote=True)
        print(transdat)
        self.assertTrue("transaction_id" in transdat.keys())
        
        q = {  'experiment_id': eid,
               'from_symbol':'USDT',
               'to_symbol': 'BTC',
               'to_quantity': 0.1,
               'type': order_type,
               'purchase_date': datetime.datetime(2020,4,1,10),
               'tag':"test submit",
               'limit_price_top': limit_price_top,
               'limit_price_bottom': limit_price_bottom,
               'limit_date': datetime.datetime(2020,4,1,12),
               'symbol_discovery':'BINANCE',                 
            }
        
        dat = pq.submit_single_market_order(q, remote=True)  
        print(dat)
        self.assertEqual(dat['status'],'pending')
        
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': datetime.datetime(2020,4,1,10,45),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,
                                                      },remote=True)
        print(dat)
        self.assertTrue(dat is True)
        
        dat = pq.find_algorithm_single_orders({'experiment_id':eid},remote=True)
    
        print(dat)
        
        self.assertTrue('avg_fill_price' in dat[0].keys())
        self.assertEqual( dat[0]['avg_fill_price'], min(limit_price_top, HighPrice) )
    
        # 2
    
        eid = str(uuid.uuid1())
        
        limit_price_top = 6310.0
        limit_price_bottom = 6295.0
        order_type = 'BUY'
        
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'USDT',
                                'quantity': 1000000,
                                'value': 1000000,
                                'date': datetime.datetime(2020,4,1,10),
                                'unit_price': 1.0,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Cash Deposit",                                
                                'api_key':api_key},remote=True)
        print(transdat)
        self.assertTrue("transaction_id" in transdat.keys())
        
        q = {  'experiment_id': eid,
               'from_symbol':'USDT',
               'to_symbol': 'BTC',
               'to_quantity': 0.1,
               'type': order_type,
               'purchase_date': datetime.datetime(2020,4,1,10),
               'tag':"test submit",
               'limit_price_top': limit_price_top,
               'limit_price_bottom': limit_price_bottom,
               'limit_date': datetime.datetime(2020,4,1,12),
               'symbol_discovery':'BINANCE',                 
            }
        
        dat = pq.submit_single_market_order(q, remote=True)  
        print(dat)
        self.assertEqual(dat['status'],'pending')
        
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': datetime.datetime(2020,4,1,10,45),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,
                                                      },remote=True)
        print(dat)
        self.assertTrue(dat is True)
        
        dat = pq.find_algorithm_single_orders({'experiment_id':eid},remote=True)
    
        print(dat)
        
        self.assertTrue('avg_fill_price' in dat[0].keys())
        self.assertEqual( dat[0]['avg_fill_price'], min(limit_price_top, HighPrice) )    
    
        # 3
    
        eid = str(uuid.uuid1())
        
        limit_price_top = 6400.0
        limit_price_bottom = 6295.0
        order_type = 'SELL'
        
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'BTC',
                                'quantity': 10,
                                'value': 500*10,
                                'date': datetime.datetime(2020,4,1,10),
                                'unit_price': 500,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Security Deposit",                                
                                'api_key':api_key},remote=True)
        print(transdat)
        self.assertTrue("transaction_id" in transdat.keys())
        
        q = {  'experiment_id': eid,
               'from_symbol':'USDT',
               'to_symbol': 'BTC',
               'to_quantity': 0.1,
               'type': order_type,
               'purchase_date': datetime.datetime(2020,4,1,10),
               'tag':"test submit",
               'limit_price_top': limit_price_top,
               'limit_price_bottom': limit_price_bottom,
               'limit_date': datetime.datetime(2020,4,1,12),
               'symbol_discovery':'BINANCE',                 
            }
        
        dat = pq.submit_single_market_order(q, remote=True)  
        print(dat)
        self.assertEqual(dat['status'],'pending')
        
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': datetime.datetime(2020,4,1,10,45),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,
                                                      },remote=True)
        print(dat)
        self.assertTrue(dat is True)
        
        dat = pq.find_algorithm_single_orders({'experiment_id':eid},remote=True)
    
        print(dat)
        
        self.assertTrue('avg_fill_price' in dat[0].keys())
        self.assertEqual( dat[0]['avg_fill_price'], max(limit_price_bottom, LowPrice) )
        
        # 4
    
        eid = str(uuid.uuid1())
        
        limit_price_top = 6400.0
        limit_price_bottom = 6285.0
        order_type = 'SELL'
        
        transdat = pq.submit_transaction({
                                'experiment_id': eid,
                                'symbol': 'BTC',
                                'quantity': 10,
                                'value': 500*10,
                                'date': datetime.datetime(2020,4,1,10),
                                'unit_price': 500,
                                'account_currency': 'USDT',
                                'type': 'algorithm',
                                'note': "Initial Security Deposit",                                
                                'api_key':api_key},remote=True)
        print(transdat)
        self.assertTrue("transaction_id" in transdat.keys())
        
        q = {  'experiment_id': eid,
               'from_symbol':'USDT',
               'to_symbol': 'BTC',
               'to_quantity': 0.1,
               'type': order_type,
               'purchase_date': datetime.datetime(2020,4,1,10),
               'tag':"test submit",
               'limit_price_top': limit_price_top,
               'limit_price_bottom': limit_price_bottom,
               'limit_date': datetime.datetime(2020,4,1,12),
               'symbol_discovery':'BINANCE',                 
            }
        
        dat = pq.submit_single_market_order(q, remote=True)  
        print(dat)
        self.assertEqual(dat['status'],'pending')
        
        dat = pq.manage_experiment({'api_key':api_key,
                                    'current_date': datetime.datetime(2020,4,1,10,45),
                                    'base_symbol':'USDT',
                                    'symbol_discovery':'BINANCE',
                                    'experiment_id':eid,
                                                      },remote=True)
        print(dat)
        self.assertTrue(dat is True)
        
        dat = pq.find_algorithm_single_orders({'experiment_id':eid},remote=True)
    
        print(dat)
        
        self.assertTrue('avg_fill_price' in dat[0].keys())
        self.assertEqual( dat[0]['avg_fill_price'], max(limit_price_bottom, LowPrice) )  
        
        #5
    
    
    
    
if __name__ == '__main__':
    unittest.main()
