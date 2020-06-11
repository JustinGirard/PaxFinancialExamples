# `get_historical_hour`

## Description

Retrieves historical hour bars for a given time interval in the past. An hour bar consists of the opening price, the closing price, the high price, and the low price for that one-hour interval.

### Arguments

**api_key :* str***
 
a valid API key

**time_in :* datetime***

the start of the interval for which to collect hour bars

**time_end :* datetime*** 

the end of the interval for which to collect hour bars

**Ticker :* str*** 

the ticker symbol of the security 


## Simple Example

    bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                    'Ticker':'BTCUSDT',
                                                                 },remote=True)
    print(bars)

## Simple Example Output

    {'_id': None, 'DateTime': datetime.datetime(2020, 4, 1, 10, 0), 'Ticker': 'BTCUSDT', 
    'ClosePrice': 6295.03, 'HighPrice': 6318.89, 'LowPrice': 6288.02, 
    'OpenPrice': 6298.74, 'close': 6295.03, 'date_time': datetime.datetime(2020, 4, 1, 10, 0), 
    'from_symbol': 'BTC', 'high': 6318.89, 'low': 6288.02, 'open': 6298.74, 
    'requested_date': '2020-06-09T21:43:53.656000', 'time': 1585735200, 
    'to_symbol': 'USDT', 'volumefrom': 19079.12, 'volumeto': 120246431.93}

## Failure Examples

    # no ticker
    # A ticker symbol must be provided.
    
    bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                                                 },remote=True)
    print(bars)
    
     
    
    # Ticker = None
    # A ticker symbol must be provided.
    
     bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                    'Ticker': None,
                                                                 },remote=True)
    print(bars)

## Failure Examples Output

    Hour Data for S&P not currently supported  File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    
    Traceback (most recent call last):
      File "/tmp/tmpjsn_a1hk.py", line 147, in process_record
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 242, in query
        return_dict =  self.query_debug(filter,source_id)
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 224, in query_debug
        res = self.query_objects[source_id].process(filter)
      File "/mnt/dev/dev/processingNetwork/ProcessingNetwork.py", line 159, in process
        feature = self.instanceMap[instanceName].process(feature,self.lastFeature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 65, in process
        self.dependencies[k].process(feature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 90, in process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 83, in process
        feature[self.settings['name']] =  self.do_process(features,self.settings)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 173, in do_process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 165, in do_process
        return self.do_input(features['input'],settings)
      File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    Exception: Hour Data for S&P not currently supported
    
    
    Hour Data for S&P not currently supported  File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    
    Traceback (most recent call last):
      File "/tmp/tmpjsn_a1hk.py", line 147, in process_record
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 242, in query
        return_dict =  self.query_debug(filter,source_id)
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 224, in query_debug
        res = self.query_objects[source_id].process(filter)
      File "/mnt/dev/dev/processingNetwork/ProcessingNetwork.py", line 159, in process
        feature = self.instanceMap[instanceName].process(feature,self.lastFeature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 65, in process
        self.dependencies[k].process(feature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 90, in process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 83, in process
        feature[self.settings['name']] =  self.do_process(features,self.settings)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 173, in do_process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 165, in do_process
        return self.do_input(features['input'],settings)
      File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    Exception: Hour Data for S&P not currently supported

## Three Examples

    bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                    'Ticker':'AAPL',
                                                                 },remote=True)
    print(bars)  
            
     
    
    
    bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                    'Ticker':'CADUSD',
                                                                 },remote=True)
    print(bars)
    
    
     
             
    bars = pq.get_historical_hour({'api_key':api_key,
                                    'time_in':datetime.datetime(2020,4,1,10),
                                    'time_end':datetime.datetime(2020,4,1,12),
                                    'Ticker':'ETHBTC',
                                                                 },remote=True)
    print(bars)

## Three Examples Output

    Hour Data for S&P not currently supported  File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    
    Traceback (most recent call last):
      File "/tmp/tmpjsn_a1hk.py", line 147, in process_record
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 242, in query
        return_dict =  self.query_debug(filter,source_id)
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 224, in query_debug
        res = self.query_objects[source_id].process(filter)
      File "/mnt/dev/dev/processingNetwork/ProcessingNetwork.py", line 159, in process
        feature = self.instanceMap[instanceName].process(feature,self.lastFeature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 65, in process
        self.dependencies[k].process(feature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 90, in process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 83, in process
        feature[self.settings['name']] =  self.do_process(features,self.settings)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 173, in do_process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 165, in do_process
        return self.do_input(features['input'],settings)
      File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    Exception: Hour Data for S&P not currently supported
    
    
    Hour Data for S&P not currently supported  File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    
    Traceback (most recent call last):
      File "/tmp/tmpjsn_a1hk.py", line 147, in process_record
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 242, in query
        return_dict =  self.query_debug(filter,source_id)
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 224, in query_debug
        res = self.query_objects[source_id].process(filter)
      File "/mnt/dev/dev/processingNetwork/ProcessingNetwork.py", line 159, in process
        feature = self.instanceMap[instanceName].process(feature,self.lastFeature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 65, in process
        self.dependencies[k].process(feature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 90, in process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 83, in process
        feature[self.settings['name']] =  self.do_process(features,self.settings)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 173, in do_process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 165, in do_process
        return self.do_input(features['input'],settings)
      File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    Exception: Hour Data for S&P not currently supported
    
    
    
    Hour Data for S&P not currently supported  File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    
    Traceback (most recent call last):
      File "/tmp/tmpjsn_a1hk.py", line 147, in process_record
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 242, in query
        return_dict =  self.query_debug(filter,source_id)
      File "/mnt/dev/dev/paxdk/PaxFinancialAPI.py", line 224, in query_debug
        res = self.query_objects[source_id].process(filter)
      File "/mnt/dev/dev/processingNetwork/ProcessingNetwork.py", line 159, in process
        feature = self.instanceMap[instanceName].process(feature,self.lastFeature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 65, in process
        self.dependencies[k].process(feature)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 90, in process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 83, in process
        feature[self.settings['name']] =  self.do_process(features,self.settings)
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 173, in do_process
        raise e
      File "/mnt/dev/dev/processingNetwork/ProcessingNode.py", line 165, in do_process
        return self.do_input(features['input'],settings)
      File "/mnt/dev/dev/FinancialAlgorithm/FinancialQueries.py", line 308, in do_input
        raise(Exception('Hour Data for S&P not currently supported'))
    Exception: Hour Data for S&P not currently supported

