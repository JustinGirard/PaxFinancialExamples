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
api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)

class TestPushPullData(unittest.TestCase):
    def test_push_pull_data(self):
        keyval = str(uuid.uuid1())
        dataval = str(uuid.uuid1())
        resp = pq.push_data({'key_field':'unit_testing_key','val':{'unit_testing_key':keyval,'unit_testing_data':dataval}},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_data({'key':{'unit_testing_key':keyval}},remote=True)
        print(dat)
        dat = dat[0]  # looking at the first element of the list should be sufficient
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('unit_testing_data' in dat.keys(), 'dict from database should contain unit_testing_data key')
        self.assertEqual(dat['unit_testing_data'],dataval,"value of dat['unit_testing_data'] should be "+str(dataval))
    
    def test_push_no_key(self):
        dataval = str(uuid.uuid1())
        resp = pq.push_data({'val':{'unit_testing_data':dataval}},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")     
  
    def test_push_keyfield_None(self):
        keyval = str(uuid.uuid1()) 
        dataval = str(uuid.uuid1())
        resp = pq.push_data({'key_field':None,'val':{'unit_testing_key':keyval,'unit_testing_data':dataval}},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")     
    
    def test_pull_key_None(self):
        resp = pq.pull_data({'key':None},remote=True)        
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")      
    
    def test_pull_empty_key(self):    
        dat = pq.pull_data({'key':{}},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")  
           
    def test_push_pull_keyval_None(self):
        keyval = None
        dataval = str(uuid.uuid1())
        resp = pq.push_data({'key_field':'unit_testing_key','val':{'unit_testing_key':keyval,'unit_testing_data':dataval}},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_data({'key':{'unit_testing_key':keyval}},remote=True)
        print(dat)
        dat = dat[0]  # looking at the first element of the list should be sufficient
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
             
    def test_push_pull_dict(self):
        keyval = str(uuid.uuid1())
        dataval = {'field1':'asdf','field2':{'field3':5,'field4':'hjkl'}}
        resp = pq.push_data({'key_field':'unit_testing_key','val':{'unit_testing_key':keyval,'unit_testing_data':dataval}},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_data({'key':{'unit_testing_key':keyval}},remote=True)
        print(dat)
        dat = dat[0]  # looking at the first element of the list should be sufficient
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('unit_testing_data' in dat.keys(), 'dict from database should contain unit_testing_data key')
        self.assertEqual(dat['unit_testing_data'],dataval,"value of dat['unit_testing_data'] should be "+str(dataval))

    def test_push_pull_array(self):
        keyval = str(uuid.uuid1())
        dataval = ['one',2,'three',4]
        resp = pq.push_data({'key_field':'unit_testing_key','val':{'unit_testing_key':keyval,'unit_testing_data':dataval}},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_data({'key':{'unit_testing_key':keyval}},remote=True)
        print(dat)
        dat = dat[0]  # looking at the first element of the list should be sufficient
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('unit_testing_data' in dat.keys(), 'dict from database should contain unit_testing_data key')
        self.assertEqual(dat['unit_testing_data'],dataval,"value of dat['unit_testing_data'] should be "+str(dataval))
        
    
if __name__ == '__main__':
    unittest.main()
