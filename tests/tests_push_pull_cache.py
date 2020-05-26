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

class TestPushPullCache(unittest.TestCase):

    def test_push_pull_cache(self):
        keyval = "unit_test"+str(uuid.uuid1())
        dataval = str(uuid.uuid1())
        resp = pq.push_cache({'key':keyval,'val':dataval},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_cache({'key':keyval},remote=True) 
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('key' in dat.keys(), 'dict from database should contain "key" key')
        self.assertTrue('val' in dat.keys(), 'dict from database should contain "val" key')
        self.assertEqual(dat['key'],keyval,"value of dat['key'] should be "+str(keyval))
        self.assertEqual(dat['val'],dataval,"value of dat['val'] should be "+str(dataval))

    def test_push_pull_dict(self):
        keyval = "unit_test"+str(uuid.uuid1())
        dataval = {'field1':'asdf','field2':'jkl;'}
        resp = pq.push_cache({'key':keyval,'val':dataval},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_cache({'key':keyval},remote=True) 
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('key' in dat.keys(), 'dict from database should contain "key" key')
        self.assertTrue('val' in dat.keys(), 'dict from database should contain "val" key')
        self.assertEqual(dat['key'],keyval,"value of dat['key'] should be "+str(keyval))
        self.assertEqual(dat['val'],dataval,"value of dat['val'] should be "+str(dataval))        
        
    def test_push_pull_nested_dict(self):
        keyval = "unit_test"+str(uuid.uuid1())
        dataval = {'field1':'asdf','field2':{'subfield1':'jkl;','subfield2':1234}}
        resp = pq.push_cache({'key':keyval,'val':dataval},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_cache({'key':keyval},remote=True) 
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('key' in dat.keys(), 'dict from database should contain "key" key')
        self.assertTrue('val' in dat.keys(), 'dict from database should contain "val" key')
        self.assertEqual(dat['key'],keyval,"value of dat['key'] should be "+str(keyval))
        self.assertEqual(dat['val'],dataval,"value of dat['val'] should be "+str(dataval))          
        
    def test_push_pull_array(self):
        keyval = "unit_test"+str(uuid.uuid1())
        dataval = ['10','12','14','16']
        resp = pq.push_cache({'key':keyval,'val':dataval},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_cache({'key':keyval},remote=True) 
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('key' in dat.keys(), 'dict from database should contain "key" key')
        self.assertTrue('val' in dat.keys(), 'dict from database should contain "val" key')
        self.assertEqual(dat['key'],keyval,"value of dat['key'] should be "+str(keyval))
        self.assertEqual(dat['val'],dataval,"value of dat['val'] should be "+str(dataval))         
        
    def test_push_pull_spurious(self):
        keyval = "unit_test"+str(uuid.uuid1())
        dataval = ['10','12','14','16']
        resp = pq.push_cache({'key':keyval,'val':dataval, 'spurious':'asdf'},remote=True)
        self.assertTrue(resp,'successful data push should return True')
        dat = pq.pull_cache({'key':keyval, 'spurious':'asdf'},remote=True) 
        self.assertTrue(len(dat)>0,'should pull non-empty data from database')
        self.assertTrue('key' in dat.keys(), 'dict from database should contain "key" key')
        self.assertTrue('val' in dat.keys(), 'dict from database should contain "val" key')
        self.assertEqual(dat['key'],keyval,"value of dat['key'] should be "+str(keyval))
        self.assertEqual(dat['val'],dataval,"value of dat['val'] should be "+str(dataval))        
        
    def test_push_ill_formed(self):
        keyval = "unit_test"+str(uuid.uuid1())
        resp = pq.push_cache({'key':keyval},remote=True)
        self.assertFalse(resp,'push without val field should return False')
         
    def test_pull_ill_formed(self):
        dataval = str(uuid.uuid1())
        dat = pq.pull_cache({'val':keyval},remote=True) 
        self.assertFalse(dat, 'pull without key field should return False')
   
        
        
    
if __name__ == '__main__':
    unittest.main()
