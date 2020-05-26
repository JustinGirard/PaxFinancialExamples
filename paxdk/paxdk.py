'''
PaxFinancialAPI

A Collection of tools used by the public to interface with Pax Financial cloud services. 
Author: Justin Girard
Licence: MIT Licence. Free to expand on the work and distribute freely.

'''

import datetime
import pandas as pd
pd.df = pd.DataFrame
import datetime, uuid, psutil, sys,os
import zipfile
from os import listdir
from os.path import isfile, join
import pickle
import base64

import json
import datetime

class jsondateencode:
    def loads(dic):
        return json.loads(dic,object_hook=datetime_parser)
    def dumps(dic):
        return json.dumps(dic,default=datedefault)

def datedefault(o):
    if isinstance(o, tuple):
        l = ['__ref']
        l = l + o
        return l
    if isinstance(o, (datetime.date, datetime.datetime,)):
        return o.isoformat()
    
def datetime_parser(dct):
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
    for k, v in dct.items():
        if isinstance(v, str) and "T" in v:
            try:
                dct[k] = datetime.datetime.strptime(v, DATE_FORMAT)
            except:
                pass
    return dct

def tdtodict(tdelta):
    '''
    Helper Function turn a timedelta into json so it can be serialized
    '''
    assert type(tdelta) == datetime.timedelta
    js_td = {
        '__day':tdelta.days,
        '__second':tdelta.seconds,
        '__microsecond':tdelta.microseconds,
    }
    return js_td  

def dicttotd(din):
    '''
    Helper Function turn a timedelta into json so it can be serialized
    '''
    assert type(din) == dict 
    assert '__day' in din
    td = datetime.timedelta(
        days = din['__day'],
        seconds = din['__second'],
        microseconds = din['__microsecond']
    )
    return td


def findclass(type_or_string,module_string=None,context=None):
        typeVar = type_or_string
        if isinstance(type_or_string, str):
            if module_string == None:
                if context:
                    typeVar = context[type_or_string]
                else:
                    typeVar = globals()[type_or_string]
            else:
                import importlib
                moduleIn = importlib.import_module(module_string)
                importlib.reload(moduleIn)
                typeVar = getattr(moduleIn ,type_or_string)
        return typeVar


class paxqueryengine():
    def __init__(self):
        self.query_definitions= {}
        self.query_objects= {}
        self.query_output_id= {}
        self.query_input_id= {}
        self.query_full_path = {}
        
        self.source_map = {}
        
        self.__settings = {}
        self.source = ''
        self.limit = ''
        self.conditions = []
        self.offset = ''
    
    def query_remote(source_id,query,url_version='stage'):
        import requests
        import pandas as pd
        url = 'https://g46w1ege85.execute-api.us-west-2.amazonaws.com/alpha/'+url_version+'/data/query'
        #print(url)
        data = {}
        data['qtype'] = source_id
        data['__encoded_query'] = paxqueryengine.do_encode(query)
        #print(data)
        r = requests.post(url, data =data)
        try:
            dat = jsondateencode.loads(r.text)
        except Exception as e :
            #print(e)
            dat = r.text
        return dat

    def do_encode(request_obj):
        serial = pickle.dumps(request_obj)
        user_data_enc = base64.b64encode(serial).decode("ascii")                   
        return user_data_enc
    
    def do_decode(data_packet):
        user_data_dev = base64.b64decode(data_packet)                   
        data2 = pickle.loads(user_data_dev)
        return data2


    def build_source(self,source_id,context_in=None,source_func=None,properties=None):
        '''
        build the data source and store the required model data
        '''
        full_str = ""
        if not source_func is None:
            try:
                if type(source_func) == str:
                    full_str = source_func
                    lst = source_func.split('.')
                    module = '.'.join(lst[0:len(lst)-1])
                    func = lst[len(lst)-1]
                    source_func = findclass(func,module,context=globals())
            except:
                return [None,None,None,None] # Cant find the function
            self.source_map[source_id] = source_func
        [networkDef,out_id,input_id,context] = self.source_map[source_id](properties)
        if context_in == None:
            context_in = {}
        context_class = globals()
        context_class.update(context)
        context_class.update(context_in)
        pn=ProcessingNetwork(networkDef,context=context_class)
        self.query_definitions[source_id] = networkDef 
        self.query_objects[source_id] = pn
        self.query_output_id[source_id] = out_id
        self.query_input_id[source_id] = input_id
        self.query_full_path[source_id] = full_str
        self.query_full_path[source_id] = full_str
        
    def query_debug(self,filter_in,source_id):
        if '__encoded_query' in filter_in:
            dic = paxqueryengine.do_decode(filter_in['__encoded_query'])
            filter_in.update(dic)
        if self.query_input_id[source_id] == None:
            filter = filter_in
        else:
            filter = {self.query_input_id[source_id]:filter_in}
        return self.query_objects[source_id].process(filter)
        
    def query(self,filter,source_id,remote=True,url_version='stage'):
        if '__encoded_query' in filter:
            dic = paxqueryengine.do_decode(filter['__encoded_query'])
            filter.update(dic)
            del(filter['__encoded_query'])
            #filter['body'] = paxqueryengine.do_encode(filter)
            #filter['content_type'] = 'application/json'
            #return(filter)
        if remote == True:
            return paxqueryengine.query_remote(source_id,filter,url_version)
        return_dict =  self.query_debug(filter,source_id)
        return return_dict[self.query_output_id[source_id]]




class PaxFinancialAPI:
    def __init__(self,context_in=None,url_version='stage',api_key = None):
        self.url_version = url_version
        self.api_key = None
        if context_in == None:
            context_in = globals()
        self.pq = paxqueryengine()
        self.current_attr = ""
        self.pq.build_source("launch_process",
                        context_in=context_in ,
                        source_func='FinancialAlgorithm.FinancialProcessQueries.build_launch_process')
        self.pq.build_source("halt_process",
                        context_in=context_in ,
                        source_func='FinancialAlgorithm.FinancialProcessQueries.build_halt_process')        
        self.pq.build_source("set_setting",
                        context_in=context_in ,
                        source_func='FinancialAlgorithm.FinancialProcessQueries.build_set_setting')        
        self.pq.build_source("balance_server",
                context_in=context_in ,
                source_func='FinancialAlgorithm.FinancialProcessQueries.build_balance_server')
        self.pq.build_source("find_processes",
                context_in=context_in ,
                source_func='FinancialAlgorithm.FinancialProcessQueries.build_find_processes')
        self.pq.build_source("get_data",
                        context_in=context_in ,
                        source_func='FinancialAlgorithm.FinancialProcessQueries.build_get_data')        
        self.pq.build_source("get_output",
                context_in=context_in ,
                source_func='FinancialAlgorithm.FinancialProcessQueries.build_get_output')

    def watch(self,q,remote=True,delay=1,offset=120):
        assert 'experiment_id' in q
        assert 'api_key' in q
        tsback = datetime.datetime.utcnow() - datetime.timedelta(seconds=offset)
        if 'api_key' not in q:
            q['api_key'] = self.api_key
        
        dat = self.get_output(q,remote=True)
        import time
        print('waiting.',end='')
        while dat == '':
            print('.',end='')
            ts = datetime.datetime.utcnow()+ datetime.timedelta(seconds=delay)
            q = { 'api_key' : q['api_key'],'experiment_id':q['experiment_id'],
                'start_date':tsback,'end_date':ts,}
            dat = self.get_output(q,remote=remote)
            time.sleep(delay)
        print(dat)
        while True:
            ts = datetime.datetime.utcnow()+ datetime.timedelta(seconds=5)
            q = { 'api_key' : q['api_key'],'experiment_id':q['experiment_id'],
                'start_date':tsback,'end_date':ts,}
            dat = self.get_output(q,remote=remote)
            tsback = datetime.datetime.utcnow() 
            print(dat)
            time.sleep(5)


    def __getattr__(self,attr):
        self.current_attr = attr
        return self.__run_query
    
    def __run_query(self,q,remote=True):
        if 'api_key' not in q:
            q['api_key'] = self.api_key
        return self.pq.query(q,self.current_attr,remote=remote,url_version=self.url_version)

print('PaxFinancialAPI v4 loaded!')