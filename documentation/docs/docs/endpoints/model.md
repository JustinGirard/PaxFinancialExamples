# `model`

## Description

Obtains the output data from a built-in machine-learning model.

### Arguments

**api_key :* str***

a valid API key

**time_in :* datetime***

start datetime
                
**time_end :* datetime***

end datetime
                
**Ticker :* str***

the ticker symbol for the security on which the model is to
 operate                

**model_id :* str***

the identifying string for the built-in model to use.
At present the only supported value is `'volume_alpha'`,
which is a volatility prediction model.
                
**version_id :* str***

the version of the model to use. At present the only 
supported value is  `'default'`.

## Simple Example

    predictions = pq.model({'api_key':api_key,
                    'time_in':datetime.datetime(2020,6,1,5),
                    'time_end':datetime.datetime(2020,6,9,12),
                    'Ticker':'BTCUSDT',
                    'model_id':'volume_alpha',
                    'version_id':'default'},remote=True)

## Simple Example Output

    {'model': [{'DateTime': datetime.datetime(2020, 6, 1, 18, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 19, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 20, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 21, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 22, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 23, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 0, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 1, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 2, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 3, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 4, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 5, 0), 'model': 1.0121240615844727}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 6, 0), 'model': 1.1079683303833008}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 7, 0), 'model': 1.6384214162826538}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 8, 0), 'model': 2.7401134967803955}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 9, 0), 'model': 2.0020201206207275}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 10, 0), 'model': 1.5636205673217773}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 11, 0), 'model': 1.478354573249817}, 
    {'DateTime': datetime.datetime(2020, 6, 2, 12, 0), 'model': 1.003968596458435}]}

## Failure Examples

    # the only value for 'model_id' supported at present is 'volume_alpha'
    
    predictions = pq.model({'api_key':api_key,
                    'time_in':datetime.datetime(2020,6,1,5),
                    'time_end':datetime.datetime(2020,6,2,12),
                    'Ticker':'BTCUSDT',
                    'model_id':'volume_beta',
                    'version_id':'default'},remote=True)
    print(predictions)

## Failure Examples Output

    {'error': 'could not locate stored model'}

## Three Examples

    # 1 a different set of start and end dates
    
    predictions = pq.model({'api_key':api_key,
                    'time_in':datetime.datetime(2020,6,1,5),
                    'time_end':datetime.datetime(2020,6,1,22),
                    'Ticker':'BTCUSDT',
                    'model_id':'volume_alpha',
                    'version_id':'default'},remote=True)
    print(predictions)
    
    
    # 2 a different set of start and end dates
    
    predictions = pq.model({'api_key':api_key,
                    'time_in':datetime.datetime(2018,7,3,10),
                    'time_end':datetime.datetime(2018,7,4,3),
                    'Ticker':'BTCUSDT',
                    'model_id':'volume_alpha',
                    'version_id':'default'},remote=True)
    print(predictions)
    
    # 3 no third example

## Three Examples Output

    {'model': [{'DateTime': datetime.datetime(2020, 6, 1, 18, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 19, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 20, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 21, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2020, 6, 1, 22, 0), 'model': 0.0}]}
    
    
    {'model': [{'DateTime': datetime.datetime(2018, 7, 3, 23, 0), 'model': 0.0},
     {'DateTime': datetime.datetime(2018, 7, 4, 0, 0), 'model': 0.0},
     {'DateTime': datetime.datetime(2018, 7, 4, 1, 0), 'model': 0.7477163076400757}, 
    {'DateTime': datetime.datetime(2018, 7, 4, 2, 0), 'model': 0.0}, 
    {'DateTime': datetime.datetime(2018, 7, 4, 3, 0), 'model': 0.8645622730255127}]}

