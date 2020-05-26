#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append("..")
sys.path.append("../..")

#from  paxnb import paxnb
import paxdk

import unittest
import uuid
import importlib
importlib.reload(paxdk)
api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)

class TestGetSendSimpleMessage(unittest.TestCase):
    def test_send_simple_message(self):
        eid = str(uuid.uuid1())
        msg = "test"+str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id':eid,'message':msg},remote=True)
        self.assertEqual(len(resp),1, "response should be a dict containing 1 field")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")
  
    def test_send_dict(self):
        eid = str(uuid.uuid1())
        msg = {'field1':'asdf','field2':'jkl;'}
        resp = pq.send_simple_message({'experiment_id':eid,'message':msg},remote=True)
        self.assertEqual(len(resp),1, "response should be a dict containing 1 field")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")

    def test_send_without_message(self): 
        eid = str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id':eid},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")     
            
    def test_send_without_eid(self): 
        msg = "test"+str(uuid.uuid1())
        resp = pq.send_simple_message({'message':msg},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")             

    def test_send_without_eid_without_message(self): 
        msg = "test"+str(uuid.uuid1())
        resp = pq.send_simple_message({},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")           
                
    def test_send_with_eid_None(self):        
        msg = "test"+str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id': None, 'message':msg},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")
        
    def test_send_with_message_None(self):
        eid = str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id':eid,'message':None},remote=True)
        self.assertEqual(len(resp),1, "response should be a dict containing 1 field")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")              

    def test_get_simple_message(self):
        eid = str(uuid.uuid1())
        msg = "test"+str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id':eid,'message':msg},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")
        resp = pq.get_simple_message({'experiment_id':eid},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('source_experiment_id' in resp.keys(),"response dict should contain 'source_experiment_id' field") 
        self.assertIsNone(resp['source_experiment_id'], "source_experiment_id should be None")
        self.assertTrue('message' in resp.keys(),"response dict should contain 'message' field")        
        
    def test_get_with_spurious_field(self):
        eid = str(uuid.uuid1())
        resp = pq.send_simple_message({'experiment_id':eid,'message':msg},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")
        resp = pq.get_simple_message({'experiment_id':eid,'spurious':'asdfasdf'},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('source_experiment_id' in resp.keys(),"response dict should contain 'source_experiment_id' field") 
        self.assertIsNone(resp['source_experiment_id'], "source_experiment_id should be None")
        self.assertTrue('message' in resp.keys(),"response dict should contain 'message' field")                
        
    def test_get_with_eid_None(self):    
        resp = pq.get_simple_message({'experiment_id':None},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")
  
    def test_get_without_eid(self):    
        resp = pq.get_simple_message({},remote=True)
        self.assertEqual(len(resp),1, "response should contain 1 field")
        self.assertTrue('error' in resp.keys(),"response dict should contain 'error' field")

    def test_get_from_empty_queue(self):
        eid = str(uuid.uuid1())
        resp = pq.get_simple_message({'experiment_id':eid},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('source_experiment_id' in resp.keys(),"response dict should contain 'source_experiment_id' field")        
        self.assertTrue('message' in resp.keys(),"response dict should contain 'message' field")
        
    def test_get_dict(self):
        eid = str(uuid.uuid1())
        msg = {'field1':'asdf','field2':'jkl;'}
        resp = pq.send_simple_message({'experiment_id':eid,'message':msg,'spurious':'asdfasdf'},remote=True)
        self.assertEqual(len(resp),1, "response should be a dict containing 1 field")
        self.assertTrue('record_id' in resp.keys(),"response dict should contain 'record_id' field")
        resp = pq.get_simple_message({'experiment_id':eid},remote=True)
        self.assertTrue(len(resp)>0, "response should be non-empty")
        self.assertTrue('source_experiment_id' in resp.keys(),"response dict should contain 'source_experiment_id' field") 
        self.assertIsNone(resp['source_experiment_id'], "source_experiment_id should be None")
        self.assertTrue('message' in resp.keys(),"response dict should contain 'message' field")
        
        
if __name__ == '__main__':
    unittest.main()
