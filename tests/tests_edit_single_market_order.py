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


class TestEditSingleMarketOrder(unittest.TestCase):
    def test_edit_market_order(self):
        
        from_symbol = 'USDT'
        to_symbol = 'BTC'
        to_quantity = 0.1
        eid = 'test_market_order'
        order_type = 'BUY'
        purchase_date = datetime.datetime.utcnow()
        
        submitted_date_approx = datetime.datetime.utcnow()
        
        dat = pq.submit_single_market_order({ 
                            'from_symbol': from_symbol,
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
        print(dat)
        order_id = dat['order_id']
        
        ###################

        limit_price_top = 100.0
        limit_price_bottom = 1.0
        
        dat = pq.edit_market_order({ 'order_id': order_id,
                                      'limit_price_top': limit_price_top,
                                      'limit_price_bottom': limit_price_bottom
                                   },remote=True)                                           
        print(dat)
        self.assertTrue('limit_price_bottom' in dat)
        self.assertEqual(dat['limit_price_bottom'],limit_price_bottom)
        self.assertTrue('limit_price_top' in dat)
        self.assertEqual(dat['limit_price_top'], limit_price_top)
        
        ####################
        
        limit_date = datetime.datetime.utcnow() + datetime.timedelta(days=2)
        dat = pq.edit_market_order({ 'order_id': order_id,
                                      'limit_date': limit_date
                                   },remote=True)                                           
        print(dat)
        
        self.assertTrue('limit_date' in dat)
        self.assertEqual(dat['limit_date'],limit_date)

        ####################
        
        limit_date = datetime.datetime.utcnow() + datetime.timedelta(days=-1)
        dat = pq.edit_market_order({ 'order_id': order_id,
                                      'limit_date': limit_date
                                   },remote=True)                                           
        print(dat)
        
        self.assertTrue('error' in dat)        
        
        ####################
        
        new_purchase_date = datetime.datetime.utcnow() + datetime.timedelta(days=-1)
        dat = pq.edit_market_order({ 'order_id': order_id,
                                     'purchase_date': new_purchase_date
                                   },remote=True)
        print(dat)
        self.assertTrue('error' in dat)
        
        #################
        
        new_from_symbol = 'CAD'
        dat = pq.edit_market_order({ 'order_id': order_id,
                                     'from_symbol': new_from_symbol         
                                    },remote=True)
        print(dat)
        self.assertTrue('error' in dat)
        
        ################
        
        new_to_symbol = 'AAPL'
        dat = pq.edit_market_order({ 'order_id': order_id,
                                     'to_symbol': new_to_symbol         
                                    },remote=True)
        print(dat)
        self.assertTrue('error' in dat)
        
        ################
        new_to_quantity = '1.5'
        dat = pq.edit_market_order({ 'order_id': order_id,
                                     'to_quantity': new_to_quantity         
                                    },remote=True)
        print(dat)
        self.assertTrue('error' in dat)
        
        ################        
        
        new_order_type = 'SELL'
        
        dat = pq.edit_market_order({ 'order_id': order_id,
                                      'type': new_order_type 
                                   },remote=True)                                           
        print(dat)
        self.assertTrue('error' in dat)
        
        
     
        
        
        
#{'from_symbol': 'USDT', 'order_id': 'ro-de7fc6e1-68cc-46a5-91aa-6d21eac576c2', 'to_symbol': 'BTC', 'to_quantity': 0.1, 'experiment_id': 'test_market_order', 'type': 'BUY', 'purchase_date': '2020-05-21T19:12:21.582226', 'submitted_date': '2020-05-21T19:12:21.582226', 'tag': 'test submit', 'limit_price_top': None, 'limit_price_bottom': None, 'limit_date': '2020-05-21T20:12:22.536036', 'simulated_price': None, 'symbol_discovery': None, 'market_price': None, 'market_status': 'pending', 'status': 'pending', 'avg_fill_price': None, 'market_avg_fill_price': None, 'transaction_fee': None, 'transaction_ids': [], '_id': None}        