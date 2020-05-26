#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("..")
sys.path.append("../..")

#from  paxnb import paxnb
import paxdk

import importlib
importlib.reload(paxdk)
import pandas as pd
 
import unittest    
import uuid    
    
api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
pq = paxdk.PaxFinancialAPI(url_version='dev',api_key=api_key)
 


class TestDownloadExperiment(unittest.TestCase):

    def test_download_financialApi(self):
        q = {'api_key':api_key,'query':{ 'status': 'running', 'name': {'$regex': '^financialApi'} }}
        dat = pq.find_processes(q,remote=True)
        df = pd.DataFrame(dat)
        eid = df['experiment_id'][0]
        arr = pq.download_experiment({ 'api_key' : api_key,'experiment_id':eid},remote=True)
 
        self.assertTrue('code' in arr, 'there should be a code field in returned object') 
        self.assertTrue('settings' in arr, 'there should be a settings field in returned object')
    
        code_snippet = '''import json
import sys
import sys
sys.path.append('../../')
sys.path.append('../../../')
from paxqueryengine.paxqueryengine import MongoCentralizedClient as MongoClient
'''

        self.assertEqual( arr['code'][:len(code_snippet)], code_snippet, 'the beginning of the experiment code is not correct')

    def test_download_nonexistent_expt(self):
        eid = uuid.uuid1()
        arr = pq.download_experiment({ 'api_key' : api_key,'experiment_id':eid},remote=True)
    
        self.assertFalse(hasattr(arr,'keys'), 'returned object should possess a keys attribute')



if __name__ == '__main__':
    unittest.main()
