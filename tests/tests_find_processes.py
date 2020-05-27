#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append("../paxdk")



#from  paxnb import paxnb
import paxdk


import unittest
import uuid
import importlib
importlib.reload(paxdk)
import pandas as pd
 
import datetime,time
start_time = time.time()
api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)
try_again = True
#paxnb.loadArguments()
 


class TestFindProcesses(unittest.TestCase):
    
    def test_retrieve_all_running(self):
        q = {'api_key':api_key,'query':{'status':'running'}}
        dat = pq.find_processes(q,remote=True)

        self.assertTrue( len(dat) > 1,  'returned data from server is too small to be correct' )
        self.assertTrue( 'experiment_id' in dat, 'should be an experiment_id field in response from server')
        self.assertTrue( 'compute_node' in dat, 'should be a compute_node field in response from server')

    def test_retrieve_by_eid(self):
        q = {'api_key':api_key,'query':{'status':'running'}}
        dat = pq.find_processes(q,remote=True)        
        df = pd.DataFrame(dat)
        eid = df['experiment_id'][0]
        q = {'api_key':api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)
        
        self.assertTrue( len(dat) > 1,  'returned data from server is too small to be correct' )
        self.assertTrue( 'experiment_id' in dat, 'should be an experiment_id field in response from server')     
        
    def test_retrieve_by_compute_node(self):    
        q = {'api_key':api_key,'query':{'status':'running'}}
        dat = pq.find_processes(q,remote=True)        
        df = pd.DataFrame(dat)
        compute_node = df['compute_node'][0]        
        q = {'api_key':api_key,'query':{'status':'running','compute_node':compute_node}}
        dat = pq.find_processes(q,remote=True)     
        
        self.assertTrue( len(dat) > 1,  'returned data from server is too small to be correct' )
        self.assertTrue( 'experiment_id' in dat, 'should be an experiment_id field in response from server')     

    def test_invalid_status(self):
        q = {'api_key':api_key,'query':{'status':'rnning'}}
        dat = pq.find_processes(q,remote=True)
 
        self.assertEqual(len(dat),0,'response from server should be empty dictionary')
 
    def test_invalid_eid(self): 
        eid = uuid.uuid1()   # since this is a unique id, no experiment should have it as an id
        q = {'api_key':api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)

        self.assertEqual(len(dat),0,'response from server should be empty dictionary')       
 
    def test_retrieve_financialApi_by_name(self):
        q = {'api_key':api_key,'query':{'name': {'$regex': '^financialApi' }}}
        dat = pq.find_processes(q,remote=True)

        self.assertTrue( len(dat) > 1,  'returned data from server is too small to be correct' )
        self.assertTrue( 'experiment_id' in dat, 'should be an experiment_id field in response from server')
        self.assertTrue( 'compute_node' in dat, 'should be a compute_node field in response from server')        
        
    def test_retrieve_by_expt_type(self):    
        q = {'api_key':api_key,'query':{'status':'running','settings.experiment_type':'financial_algorithm'}}
        dat = pq.find_processes(q,remote=True)
        
        self.assertTrue( len(dat) > 1,  'returned data from server is too small to be correct' )
        self.assertTrue( 'experiment_id' in dat, 'should be an experiment_id field in response from server')
        self.assertTrue( 'compute_node' in dat, 'should be a compute_node field in response from server')          

    def test_retrieve_by_started(self):    
        dt = datetime.datetime.utcnow()-datetime.timedelta(days=30)
        q = {'api_key':api_key,'query':{'status':'running','started':{'$gt':dt}}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 

    def test_retrieve_by_finished(self):
        dt = datetime.datetime.utcnow()-datetime.timedelta(days=30)
        q = {'api_key':api_key,'query':{'status':'running','finished':{'$gt':dt}}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 

    def test_retrieve_by_submitted(self):
        dt = datetime.datetime.utcnow()-datetime.timedelta(days=30)
        q = {'api_key':api_key,'query':{'status':'running','submitted':{'$gt':dt}}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 

    def test_retrieve_by_last_contacted(self):
        dt = datetime.datetime.utcnow()-datetime.timedelta(minutes=10)
        q = {'api_key':api_key,'query':{'status':'running','last_contacted':{'$gt':dt}}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 

    def test_retrieve_auto_restart_true(self):
        q = {'api_key':api_key,'query':{'status':'running','auto_restart':True}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 

    def test_retrieve_auto_restart_false(self):
        q = {'api_key':api_key,'query':{'status':'running','auto_restart':False}}
        dat = pq.find_processes(q,remote=True)
        # we have to determine what valid/invalid responses are here
        # both empty and non-empty responses might be correct 
 

if __name__ == '__main__':
    unittest.main()
    
