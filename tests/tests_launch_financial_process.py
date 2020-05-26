import unittest
import datetime, uuid, psutil, sys,os,time
import uuid, psutil, sys,os
import sys
import importlib
sys.path.append('..')
sys.path.append('../../')
#from  paxqueryengine.paxqueryengine  import mongoquerymanager,paxqueryengine  
import paxdk
pq = paxdk.PaxFinancialAPI(url_version='dev')
api_key = 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a'
import pandas as pd
mid = 'market_paper_simulation'
aid ='automated_unit_test'
import uuid

#
#
# This test is the first paper trading test on the platform. It assumes that all other tests have run with success. 
#
#

class TestLaunchFinancialProcess(unittest.TestCase):
    def create_realtime_process(self,minutes=5,record_steps=0):

        nw =datetime.datetime.utcnow()
        tm = datetime.datetime.utcnow()
        st =tm 
        et = tm + datetime.timedelta(minutes=minutes)
        
        networkDef = {'marketos': {'dependencies': {'experiment_id': ['__ref', 'experiment_id'],
                               'fill_field': 'OpenPrice',
                               'input': {'prices': ['__ref', 'price', 'output'],
                                         'time_in': ['__ref',
                                                     'time_emitter',
                                                     'output']},
                               'mos_settings': {'holdings': {'cash': 1000}}},
              'name': 'marketos',
              'type': 'MarketOsRunner'},
 'mindiff': {'dependencies': {'field': 'DateTime',
                              'input': ['__ref', 'percentagefilter', 'output'],
                              'new_field': 'MinuteDelta'},
             'name': 'mindiff',
             'type': 'MinutesDiff'},
 'percentagefilter': {'dependencies': {'fields': ['OpenPrice'],
                                       'input': ['__ref', 'price', 'output']},
                      'name': 'percentagefilter',
                      'type': 'PercentageFilter'},
 'price': {'dependencies': {'input': {'Ticker': ['__ref',
                                                 'securities_emitter',
                                                 'output'],
                                      'bars': 5,
                                      'fields': ['OpenPrice',
                                                 'ClosePrice',
                                                 'DateTime'],
                                      'resolution': 'hour',
                                      'time': ['__ref',
                                               'time_emitter',
                                               'output']}},
           'name': 'price',
           'type': 'PriceEmitter'},
 'securities_emitter': {'dependencies': {'input': ['BTCUSDT']},
                        'name': 'securities_emitter',
                        'type': 'SecuritiesEmitter'},
 'strategy': {'dependencies': {'experiment_id': ['__ref', 'experiment_id'],
                               'input': {'api_key': 'pkey-a0f8540cacc41427ae251101ce1dc1f612068ffcbe9801f27294251a',
                                         'buy_low': True,
                                         'denom_days': 230.440141472798,
                                         'do_pl_hedge': True,
                                         'lockout_days': 30.278463148032007,
                                         'lockout_max': 1.362651617280004,
                                         'lockout_min': 0.00150069551104,
                                         'marketos': ['__ref', 'marketos'],
                                         'numer_days': 176.95501330710414,
                                         'pl2_end_date_delta_hours': 0,
                                         'pl2_hedge_attack': 11.378747959339542,
                                         'pl2_hedge_x_bias': 4.734250353770499,
                                         'pl2_start_date_delta_hours': 305.15804590380424,
                                         'pl_benchmark_symbol': 'BTCUSDT',
                                         'pl_end_date_delta_hours': 0,
                                         'pl_hedge_attack': 17.612850447751992,
                                         'pl_hedge_symbol': 'cash',
                                         'pl_hedge_x_bias': 6.994176218269176,
                                         'pl_start_date_delta_hours': 597.3463268479491,
                                         'rebalance_on_minimum_delta': 0.13358900826218892,
                                         'securities': ['__ref',
                                                        'securities_emitter',
                                                        'output'],
                                         'std_factor': 5.783288996250202,
                                         'target_sec': 'BTCUSDT',
                                         'time': ['__ref',
                                                  'time_emitter',
                                                  'output']}},
              'name': 'strategy',
              'type': 'HourlyRebalance'},
 'time_emitter': {'dependencies': 
                       {'delay': 0,
               'end_date': '2020-04-02T20:00:00',
               'increment': ['minutes', 120],
               'input': None,
               'mode': 'backtest',
               'start_date': '2020-04-01T10:00:00'},
      'name': 'time_emitter',
      'type': 'TimeEmitter'}
                     
                     }
        
        
        codeString = '''
import inspect
from processTemplate.JEFProcessHandle import JEFProcessHandle
import uuid, psutil, sys,os
sys.path.append('../../')
from processingNetwork.ProcessingNode import ProcessingNode
from processingNetwork.PipeProcessingNode import PipeProcessingNode
from CryptoAlgorithm.CryptoQueries import CryptoExecutionsEmitter
import pandas
import datetime
# 1 - stop reinniting the PaxAPI
# 2 - rel_mean_std can use present data, too
class HourlyRebalance(ProcessingNode):
    def isolateFlows(pq,feature):
        cols = pq.relative_mean_std_grid_hourly(feature,remote=False)
        df = pd.DataFrame(cols)[['OpenPrice_mean','Ticker']]
        df = df[df['OpenPrice_mean'].notnull()]

        flows = []
        for i,row_denom in df.iterrows():
            for i,row_num in df.iterrows():
                flow = {}
                flow['Ticker_from'] = row_num['Ticker']
                flow['Ticker_to'] = row_denom['Ticker'] 
                flow['OpenPrice_mean_from'] = row_num['OpenPrice_mean']
                flow['OpenPrice_mean_to'] = row_denom['OpenPrice_mean']
                flow['flow'] = flow['OpenPrice_mean_from']/flow['OpenPrice_mean_to']
                flows.append(flow)
        df_flow = pd.DataFrame(flows)       
        return df_flow

    def holdingsFromFlows(df_flow,flow_bias,cash):
        df_flow = df_flow.sort_values(['flow'])
        df_flow = df_flow[df_flow['flow'] > flow_bias]
        df_flow['holds'] = df_flow['flow']
        df_flow['holds'] = df_flow['holds']/df_flow['flow'].sum()
        #display(df_flow)

        # From USDT (absolute)
        target_holding_ratio = {}
        for i,row in df_flow.iterrows():
            if row['Ticker_to'] not in target_holding_ratio:
                target_holding_ratio[row['Ticker_to']] = 0
            target_holding_ratio[row['Ticker_to']] = target_holding_ratio[row['Ticker_to']] + row['holds']
            target_holding_ratio[row['Ticker_to']+'_value'] = row['holds']*cash
        return target_holding_ratio

    
    def getMarketHoldingsStats():
        mos = MarketOsRunner.GetInstance()
        holds_now = mos.getHoldings()
        holds_value = {}
        holds_ratio = {}
        value_sum = 0
        for sym in holds_now: 
            if mos.getAsk(sym):
                holds_value[sym] = mos.getAsk(sym)*holds_now[sym]
                value_sum = value_sum  + holds_value[sym]
            elif sym =='cash':
                holds_value[sym] = (1.0)*holds_now[sym]
                value_sum = value_sum  + holds_value[sym]
                
        for sym in holds_now: 
            holds_ratio[sym] = holds_value[sym]/value_sum 
        return {'holds_now':holds_now,'holds_value':holds_value,'holds_ratio':holds_ratio}
    
    def getRatioDeltas(heldRatio,targetRatio):
        orderRatios = {}
        for sym in targetRatio:
            if not sym in heldRatio:
                orderRatios[sym] = targetRatio[sym]
            else:
                orderRatios[sym] = targetRatio[sym] - heldRatio[sym]
        for sym in heldRatio:
            if not sym in targetRatio:
                orderRatios[sym] = 0.0 - heldRatio[sym]
        return orderRatios

    def getRawHoldings(pq,feature):
        dat = pq.relative_mean_std_grid_hourly(q=feature,remote=False)
        cols = pd.DataFrame(dat [0])
        num = pd.DataFrame(dat [1])
        row = {
            'ClosePrice_mean':1.0,
            'ClosePrice_std':0,
            'HighPrice_mean':1.0,
            'HighPrice_std':0,
            'LowPrice_mean':1.0,
            'LowPrice_std':0,
            'OpenPrice_mean':1.0,
            'OpenPrice_std':0,
            'Ticker':'cash'        }
        cols = cols.append(row,ignore_index=True)
        denom = pd.DataFrame(dat [2])

        cols['raw_holds'] = cols['OpenPrice_mean']
        cols['raw_holds'] = cols['raw_holds']*cols['raw_holds']
        
        std_factor = 1.0
        if feature['std_factor'] > 0:
            std_factor =(cols['OpenPrice_std']*feature['std_factor']+0.1)

        if feature['buy_low'] == True:
            cols['raw_holds'] = (1.0/cols['raw_holds'])*std_factor
        else:
            cols['raw_holds'] = (cols['raw_holds'])*std_factor
        cols['raw_holds'] = cols['raw_holds']/cols['raw_holds'].sum()
        return [cols, num, denom]
    def getSelfPL(pq,api_key,eid,start_date,end_date,currenttime,context,label):
        mos = MarketOsRunner.GetInstance()
        vt = mos.getValueTotal()
        if vt == None:
            print("FAILED VALUE TOTAL")
            return 1.0
        try:
            context['vhist'+label]
        except:
            context['vhist'+label] = []
        if not currenttime == None:
            context['vhist'+label].append({'date':currenttime,'value_total':vt})
        if len(context['vhist'+label]) > 500:
            context['vhist'+label].pop(0)
        df = pd.DataFrame(context['vhist'+label])
        df = df[df['date']>start_date]
        df = df[df['date']<end_date]
        if len(df.index) < 2:
            print("Got no bars!")
            return 1.0
        # Just making sure the data is sorted correctly....
        df = df.sort_values(['date'])
        assert df['date'].iloc[len(df['date'])-1] >  df['date'].iloc[0]
        pl = df['value_total'].iloc[len(df['value_total'])-1]/df['value_total'].iloc[0]
 
        #try:
        #    ohlc_price = pq.get_market_raw_value_data(q={ 'api_key' : api_key,'experiment_id':eid,'time_in':start_date,'time_end':end_date},remote=False)
        #    df = pd.DataFrame(ohlc_price['value']).T
        #    pl = df['value_total'][len(df['value_total'])-1]/df['value_total'][0]
        #except Exception as e:
        #    print('getSelfPL ex:')
        #    print(e)
        #    import traceback
        #    traceback.print_exc()
        #    return None
        return pl

    def getSymbolPl(pq,api_key,time_start,time_end,symbol):
        f = {'api_key':api_key,'time_in':time_start, 'time_end':time_end ,'Ticker':'BTCUSDT'}
        dat = pq.get_historical_hour(f,remote=False)
        df = pd.DataFrame(dat)
        df = df.sort_values(['DateTime'])
        assert df['DateTime'].iloc[len(df['DateTime'])-1] > df['DateTime'].iloc[0] 
        pl = df['OpenPrice'].iloc[len(df['OpenPrice'])-1] / df['OpenPrice'].iloc[0] 
        return pl
    
    def getPlAlpha(pq,api_key,eid,start_date,end_date,currenttime,context,benchmark,alpha_start_date,alpha_end_date):
        self_pl = HourlyRebalance.getSelfPL(pq,api_key,eid,start_date,end_date,currenttime,context)
        
        alpha_pl = HourlyRebalance.getSelfPL(pq,api_key,eid,alpha_start_date,alpha_end_date,None,context)
        benchmark_pl = HourlyRebalance.getSymbolPl(pq,api_key,alpha_start_date,alpha_end_date,benchmark)
        alpha = alpha_pl/benchmark_pl 
        return [self_pl,alpha]
        
    
    def getInvestHedgeFraction(pl,hedge_attack_power=4,hedge_x_bias=1.0):
        invf = 1.0
        print('getInvestHedgeFraction')
        print('pl ', str(pl))
        print('att ', str(hedge_attack_power))
        print('xb ',  str(hedge_x_bias))
        
        if not pl == None: 
            v = pl
            invf = hedge_x_bias/(v**hedge_attack_power+0.5)
            if invf>1:
                invf = 1.0
        frac_invest = invf
        frac_hedge = 1.0 - invf
        print('results')
        print(str(frac_invest))
        print(str(frac_hedge))
        
        return frac_invest,frac_hedge 

    def logExperimentSignals(api_key,pq,date,eid,data):
        log = {
        'DateTime': date,
        'experiment_id' :eid,
        'data_type' :'experiment_signals',
        'log_key':'experiment_signal_'+str(date)+'_'+eid
        }
        data.update(log)
        q = {'api_key' : api_key,'key_field':'log_key','val':data}
        dat = pq.push_data(q,remote=False)
    
    def adjustTargetHoldingsWithInvestHedgeFractions(pl,target_holds_ratio,hedgesymbol,frac_invest,frac_hedge):
        if not pl == None:
            target_holds_ratio_new = {}
            for k in target_holds_ratio:
                if k == hedgesymbol:
                    target_holds_ratio_new[k] = target_holds_ratio[k]* frac_invest + 1.0*frac_hedge
                else:
                    target_holds_ratio_new[k] = target_holds_ratio[k]* frac_invest + 0.0*frac_hedge
            target_holds_ratio = target_holds_ratio_new
            print('new:')
            print(target_holds_ratio)
        return target_holds_ratio
        
    def do_input(self,feature,context):
        import pprint
        import datetime
        import tracemalloc
        tracemalloc.start()
        import time
        start_time = time.time()
        start_time_total = time.time()
        if not 'lockout_until' in context:
            context['lockout_until'] =  feature['time'] - datetime.timedelta(days=1)
            
        try: 
            a = HourlyRebalance.pq
        except Exception as e:
            print(e)
            HourlyRebalance.pq = PaxFinancialAPI.PaxFinancialAPI(url_version='dev')
            
        mos = MarketOsRunner.GetInstance()
        holds_now = mos.getHoldings()
        nw =   feature['time']
        syms = feature['securities']
        
        
        time_in_num = nw - datetime.timedelta(days=feature['numer_days'])
        time_end_num = nw 
        time_in_denom = nw - datetime.timedelta(days=feature['denom_days'])
        time_end_denom = nw 
        
        feature_flow = {'api_key':feature['api_key'], 
                   'time_in_num':time_in_num,  'time_end_num':time_end_num ,
                   'time_in_denom':time_in_denom,  'time_end_denom':time_end_denom ,
                   'symbols':syms,
                    'std_factor':feature['std_factor'],
                    'buy_low':feature['buy_low'],
                       }
        cash = holds_now['cash']
        
        #print("G Current Execution time is  "+ str(time.time()-start_time))
            
        start_date = nw - datetime.timedelta(hours=feature['pl_start_date_delta_hours'])
        end_date = nw - datetime.timedelta(hours=feature['pl_end_date_delta_hours'])
        start_date_2 = nw - datetime.timedelta(hours=feature['pl2_start_date_delta_hours'])
        end_date_2 = nw - datetime.timedelta(hours=feature['pl2_end_date_delta_hours'])
        
        
        pl = None
        pl2 = None
        hedgesymbol = feature['pl_hedge_symbol']
        frac_invest = 1.0
        frac_hedge = 0.0
        start_time = time.time()
        frac_hedge_pl=0.0
        frac_hedge_pl2=0.0
        
        
        
        
        if feature['do_pl_hedge'] == True:
            pl = HourlyRebalance.getSelfPL(HourlyRebalance.pq,feature['api_key'],context['experiment_id'],
                                           start_date,end_date,feature['time'],context,'pl')
            pl2 = HourlyRebalance.getSelfPL(HourlyRebalance.pq,feature['api_key'],context['experiment_id'],
                                           start_date_2,end_date_2,feature['time'],context,'pl2')

            print("Total getSelfPL Execution time is  "+ str(time.time()-start_time))
            start_time = time.time()
            [frac_invest_pl,frac_hedge_pl] = HourlyRebalance.getInvestHedgeFraction(pl,
                                                                              hedge_attack_power=feature['pl_hedge_attack'],
                                                                              hedge_x_bias=feature['pl_hedge_x_bias'])
            [frac_invest_pl2,frac_hedge_pl2] = HourlyRebalance.getInvestHedgeFraction(pl2,
                                                                              hedge_attack_power=feature['pl2_hedge_attack'],
                                                                              hedge_x_bias=feature['pl2_hedge_x_bias'])
            
            frac_hedge = max([frac_hedge_pl,frac_hedge_pl2])
            frac_invest = 1.0 - frac_hedge  
            print("Total getInvestHedgeFraction Execution time is  "+ str(time.time()-start_time))
            start_time = time.time()
        if context['lockout_until'] <  feature['time']:
            if pl > feature['lockout_max'] or pl2 > feature['lockout_max']: #We have recently made 10%. It might be prudent to lock out
                context['lockout_until'] =  feature['time'] + datetime.timedelta(days=feature['lockout_days'])
            if pl < feature['lockout_min'] or pl2 < feature['lockout_min']: #We have recently made 10%. It might be prudent to lock out
                context['lockout_until'] =  feature['time'] + datetime.timedelta(days=feature['lockout_days'])
        lockout_hedge = 0
        if context['lockout_until'] > feature['time']:
            frac_invest = 0.0
            frac_hedge = 1.0
            lockout_hedge =1
        #print("F Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        rawHoldData =  HourlyRebalance.getRawHoldings(HourlyRebalance.pq,feature_flow)
        print("Total getHoldings Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        
        holds = rawHoldData[0]
        num = rawHoldData[1]
        denom = rawHoldData[2]
        
        target_holds_ratio = {} 
        for i,row in holds.iterrows():
            target_holds_ratio[row['Ticker']] = row['raw_holds']
        #print("---------------------------------")
        #print("---------------------------------")
        #print("---------------------------------")
        #print(feature['time'])
        #print(target_holds_ratio)
        print("E Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        target_holds_ratio =  HourlyRebalance.adjustTargetHoldingsWithInvestHedgeFractions(pl,
                                                                           target_holds_ratio,
                                                                           hedgesymbol,
                                                                           frac_invest,
                                                                           frac_hedge)

        #print('new target:')
        #print(target_holds_ratio)
        #print("D Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()

        
        dat = HourlyRebalance.getMarketHoldingsStats()
        holds_ratio = dat['holds_ratio'] 
        holds_value = dat['holds_value'] 
        total_value =  sum(list(holds_value.values()))
        #print('holds now:')
        #print(holds_ratio)
        
        orderDelta = HourlyRebalance.getRatioDeltas(holds_ratio,target_holds_ratio)
        #print("C Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        print(orderDelta)
        orderValue = {}
        orderShares = {}
        delta_abs_sum = 0.0
        for k in orderDelta:
            delta_abs_sum = delta_abs_sum + abs(float(orderDelta[k]))
        
        

        log_data = {'alpha_pl':pl,
                    'frac_invest':frac_invest,
                    'frac_hedge':frac_hedge,
                    'delta_abs_sum':delta_abs_sum,
                    'frac_hedge_pl':frac_hedge_pl,
                    'frac_hedge_pl_2':frac_hedge_pl2,
                    'lockout_hedge':lockout_hedge, 
                    'pl':pl,
                    'pl2':pl2
                   }
        for k in holds_now:
            log_data['hold_'+k] =  holds_now[k]
        for k in holds_value:
            log_data['value_'+k] =  holds_value[k]
        for k in holds_ratio:
            log_data['ratio_'+k] =  holds_ratio[k]
            
        HourlyRebalance.logExperimentSignals(feature['api_key'],
                                             HourlyRebalance.pq,
                                             feature['time'],
                                             context['experiment_id'],
                                             log_data)
        
        
        if delta_abs_sum< feature['rebalance_on_minimum_delta']:
            print('sk sum ',str(delta_abs_sum), ' min ',str(feature['rebalance_on_minimum_delta']))
            print(orderDelta)
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
            print("Total Current Execution time is  "+ str(time.time()-start_time_total))
            tracemalloc.stop()        
            
            return None
        #print("B Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        for k in orderDelta:
            if k != 'cash' and mos.getAsk(k): 
                orderValue[k] = total_value*orderDelta[k]
                orderShares[k] = orderValue[k]/mos.getAsk(k)
            elif  k != 'cash':
                orderValue[k] = None
                orderShares[k] = None
            else:
                orderValue[k] = total_value*orderDelta[k]
                orderShares[k] = orderValue[k]                
        #print("A Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
                
        #print('*')
        #print(orderDelta)
        #print(orderValue)
        #print(orderShares)
        #print('*')
        for sec in orderShares:
            shares =orderShares[sec]
            if sec != 'cash' and shares and mos.getAsk(sec):
                if abs(shares*mos.getAsk(sec)) > 20:
                    mos.order(security=sec,amount=shares)
            if sec == 'cash':
                pass #Taken care of by selling out of other positions in the != cash category
        #mos.order(security,amount,expire_security_value=None,expire_security_holding_rate=None,originalShareValue=None,bracket_order = None):
        # order(self,security,amount,expire_security_value=None,expire_security_holding_rate=None,originalShareValue=None,bracket_order = None):
        # avg_now = mos.get_price_avg(feature,context,start_date,limit_timedelta,target_sec)
        # mos.do_order_bracket(target_sec,
        #                                    testOrder=False,
        #                                    limit_max = bracket_limit_max,
        #                                    limit_min = bracket_limit_min,
        #                                    limit_timedelta=datetime.timedelta(days=bracket_limit_days),
        #                                    trade_size = holds['cash']*invest_fraction, # Grab 10 shares
        #                                    order_type = "buy",
        #                                    )                      
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        print("Total Current Execution time is  "+ str(time.time()-start_time_total))
        start_time = time.time()
        tracemalloc.stop()
        
        return None
    
import pprint,json

# Add to PL code - code that estimates value of  PL before data comes in based on avg os securities 
'''
        return [networkDef,codeString]
    
    def wait_for_process_to_start(self,eid,pause=5,quit=160):
        status = None
        count = 0
        while not status in ['running','completed']: 
            q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
            dat = pq.find_processes(q,remote=True)
            try:
                status = list(pd.DataFrame(dat)['status'])[0]
            except Exception as e:
                print(dat)
                raise e
            print('.',end='')
            time.sleep(pause)
            count = count + pause
            if count > quit:
                break
        print('|')
        return status
    
    def wait_for_process_to_finish(self,eid,pause=5,quit=280):
        status = None
        count = 0
        while not status in ['completed','crashed','halted','cleared']: 
            q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
            dat = pq.find_processes(q,remote=True)
            try:
                status = list(pd.DataFrame(dat)['status'])[0]
            except Exception as e:
                print(dat)
                raise e
            print('.',end='')
            time.sleep(pause)
            count = count + pause
            if count > quit:
                break
        print('|')
        return status
    
    def launch_a_test_process(self,minutes=1000,record_steps=0):
        financialNetworkDef,codeString = self.create_realtime_process(minutes,record_steps)
        q = { 'api_key' : api_key,'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        self.assertEqual('experiment_id' in dat, True, 'Could not start process')
        eid = dat['experiment_id']
        print(eid)
        status = self.wait_for_process_to_start(eid)
        return [status,eid]
    
    def clean_up_data(self):
        q = { 'api_key' : api_key,'nameSearch':'test_financial_process_simulation'}
        procs = pq.find_processes(q,remote=True)
        procs = pd.DataFrame(procs)
        procs = list(procs['experiment_id'])
        print("procs=")
        print(procs)        
        for eid in procs:
            print(eid)
            dat = pq.delete_process(q = { 'api_key' : api_key,'experiment_id':eid},remote=True)
            print(dat)
            q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
            dat = pq.find_processes(q,remote=True)
            print(dat)
            self.assertEqual(len(dat), 0, 'Could not delete process '+ str(eid) )
        
    def clean_old_test_jobs(self):
        dat = pq.find_processes({'api_key' : api_key,'nameSearch':'test_financial_process_simulation'})
        #display(pd.DataFrame(dat))
        
        print("cleaning old test jobs")
        
        for eid in list(pd.DataFrame(dat)['experiment_id']):
            q = {'api_key' : api_key,'experiment_id':eid,
                      'key':'auto_restart','val':False}
            dat = pq.set_setting(q,remote=True)
            q = {'api_key' : api_key,'experiment_id':eid}
            dat = pq.halt_process(q,remote=True)
            print(eid)
        
    def test_financial_process_simulation(self): #######
        #self.clean_old_test_jobs()
        print("Testing basic paper process")
        #
        # 1. Start Normal Finish After Five Minuutes
        min_date = datetime.datetime.utcnow()
        [status,eid] = self.launch_a_test_process(2)
        self.assertEqual(status in ['running','completed'], True, 'Could not start process successfully ' + str(status))
        status = self.wait_for_process_to_finish(eid)
        print("Status is " + status)
        try:
            assert status in ['completed']
        except:
            print('Halted')
            pq.halt_process({'api_key':api_key,'experiment_id':eid})
        self.assertEqual(status in ['completed', 'halted'], True, 'Could not finish process correctly!')
        #q = {'api_key':api_key,'experiment_id':eid}
        #data = pq.get_data(q,remote=True)
        #df = pd.DataFrame(data)
        #mk = pd.DataFrame(df['marketos'])
        #max_date = mk['date'].max()
        #print('Finished ', str(min_date), " ", str(max_date), " ", str(max_date - min_date))
 
        self.clean_up_data()
        
        #self.assertEqual( len(orders), 1)
    
    
    def test_launch_crash_process(self):
        minutes=5
        record_steps=0
        min_date = datetime.datetime.utcnow()
        financialNetworkDef,codeString = self.create_realtime_process(minutes,record_steps)
        codeString = '''
import inspect
from processTemplate.JEFProcessHandle import JEFProcessHandle
import uuid, psutil, sys,os
sys.path.append('../../')
from processingNetwork.ProcessingNode import ProcessingNode
from processingNetwork.PipeProcessingNode import PipeProcessingNode
from CryptoAlgorithm.CryptoQueries import CryptoExecutionsEmitter
import pandas
import datetime
# 1 - stop reinniting the PaxAPI
# 2 - rel_mean_std can use present data, too
class HourlyRebalance(ProcessingNode):
    def isolateFlows(pq,feature):
        cols = pq.relative_mean_std_grid_hourly(feature,remote=False)
        df = pd.DataFrame(cols)[['OpenPrice_mean','Ticker']]
        df = df[df['OpenPrice_mean'].notnull()]

        flows = []
        for i,row_denom in df.iterrows():
            for i,row_num in df.iterrows():
                flow = {}
                flow['Ticker_from'] = row_num['Ticker']
                flow['Ticker_to'] = row_denom['Ticker'] 
                flow['OpenPrice_mean_from'] = row_num['OpenPrice_mean']
                flow['OpenPrice_mean_to'] = row_denom['OpenPrice_mean']
                flow['flow'] = flow['OpenPrice_mean_from']/flow['OpenPrice_mean_to']
                flows.append(flow)
        df_flow = pd.DataFrame(flows)       
        return df_flow

    def holdingsFromFlows(df_flow,flow_bias,cash):
        df_flow = df_flow.sort_values(['flow'])
        df_flow = df_flow[df_flow['flow'] > flow_bias]
        df_flow['holds'] = df_flow['flow']
        df_flow['holds'] = df_flow['holds']/df_flow['flow'].sum()
        #display(df_flow)

        # From USDT (absolute)
        target_holding_ratio = {}
        for i,row in df_flow.iterrows():
            if row['Ticker_to'] not in target_holding_ratio:
                target_holding_ratio[row['Ticker_to']] = 0
            target_holding_ratio[row['Ticker_to']] = target_holding_ratio[row['Ticker_to']] + row['holds']
            target_holding_ratio[row['Ticker_to']+'_value'] = row['holds']*cash
        return target_holding_ratio

    
    def getMarketHoldingsStats():
        mos = MarketOsRunner.GetInstance()
        holds_now = mos.getHoldings()
        holds_value = {}
        holds_ratio = {}
        value_sum = 0
        for sym in holds_now: 
            if mos.getAsk(sym):
                holds_value[sym] = mos.getAsk(sym)*holds_now[sym]
                value_sum = value_sum  + holds_value[sym]
            elif sym =='cash':
                holds_value[sym] = (1.0)*holds_now[sym]
                value_sum = value_sum  + holds_value[sym]
                
        for sym in holds_now: 
            holds_ratio[sym] = holds_value[sym]/value_sum 
        return {'holds_now':holds_now,'holds_value':holds_value,'holds_ratio':holds_ratio}
    
    def getRatioDeltas(heldRatio,targetRatio):
        orderRatios = {}
        for sym in targetRatio:
            if not sym in heldRatio:
                orderRatios[sym] = targetRatio[sym]
            else:
                orderRatios[sym] = targetRatio[sym] - heldRatio[sym]
        for sym in heldRatio:
            if not sym in targetRatio:
                orderRatios[sym] = 0.0 - heldRatio[sym]
        return orderRatios

    def getRawHoldings(pq,feature):
        dat = pq.relative_mean_std_grid_hourly(q=feature,remote=False)
        cols = pd.DataFrame(dat [0])
        num = pd.DataFrame(dat [1])
        row = {
            'ClosePrice_mean':1.0,
            'ClosePrice_std':0,
            'HighPrice_mean':1.0,
            'HighPrice_std':0,
            'LowPrice_mean':1.0,
            'LowPrice_std':0,
            'OpenPrice_mean':1.0,
            'OpenPrice_std':0,
            'Ticker':'cash'        }
        cols = cols.append(row,ignore_index=True)
        denom = pd.DataFrame(dat [2])

        cols['raw_holds'] = cols['OpenPrice_mean']
        cols['raw_holds'] = cols['raw_holds']*cols['raw_holds']
        
        std_factor = 1.0
        if feature['std_factor'] > 0:
            std_factor =(cols['OpenPrice_std']*feature['std_factor']+0.1)

        if feature['buy_low'] == True:
            cols['raw_holds'] = (1.0/cols['raw_holds'])*std_factor
        else:
            cols['raw_holds'] = (cols['raw_holds'])*std_factor
        cols['raw_holds'] = cols['raw_holds']/cols['raw_holds'].sum()
        return [cols, num, denom]
    def getSelfPL(pq,api_key,eid,start_date,end_date,currenttime,context,label):
        mos = MarketOsRunner.GetInstance()
        vt = mos.getValueTotal()
        if vt == None:
            print("FAILED VALUE TOTAL")
            return 1.0
        try:
            context['vhist'+label]
        except:
            context['vhist'+label] = []
        if not currenttime == None:
            context['vhist'+label].append({'date':currenttime,'value_total':vt})
        if len(context['vhist'+label]) > 500:
            context['vhist'+label].pop(0)
        df = pd.DataFrame(context['vhist'+label])
        df = df[df['date']>start_date]
        df = df[df['date']<end_date]
        if len(df.index) < 2:
            print("Got no bars!")
            return 1.0
        # Just making sure the data is sorted correctly....
        df = df.sort_values(['date'])
        assert df['date'].iloc[len(df['date'])-1] >  df['date'].iloc[0]
        pl = df['value_total'].iloc[len(df['value_total'])-1]/df['value_total'].iloc[0]
 
        #try:
        #    ohlc_price = pq.get_market_raw_value_data(q={ 'api_key' : api_key,'experiment_id':eid,'time_in':start_date,'time_end':end_date},remote=False)
        #    df = pd.DataFrame(ohlc_price['value']).T
        #    pl = df['value_total'][len(df['value_total'])-1]/df['value_total'][0]
        #except Exception as e:
        #    print('getSelfPL ex:')
        #    print(e)
        #    import traceback
        #    traceback.print_exc()
        #    return None
        return pl

    def getSymbolPl(pq,api_key,time_start,time_end,symbol):
        f = {'api_key':api_key,'time_in':time_start, 'time_end':time_end ,'Ticker':'BTCUSDT'}
        dat = pq.get_historical_hour(f,remote=False)
        df = pd.DataFrame(dat)
        df = df.sort_values(['DateTime'])
        assert df['DateTime'].iloc[len(df['DateTime'])-1] > df['DateTime'].iloc[0] 
        pl = df['OpenPrice'].iloc[len(df['OpenPrice'])-1] / df['OpenPrice'].iloc[0] 
        return pl
    
    def getPlAlpha(pq,api_key,eid,start_date,end_date,currenttime,context,benchmark,alpha_start_date,alpha_end_date):
        self_pl = HourlyRebalance.getSelfPL(pq,api_key,eid,start_date,end_date,currenttime,context)
        
        alpha_pl = HourlyRebalance.getSelfPL(pq,api_key,eid,alpha_start_date,alpha_end_date,None,context)
        benchmark_pl = HourlyRebalance.getSymbolPl(pq,api_key,alpha_start_date,alpha_end_date,benchmark)
        alpha = alpha_pl/benchmark_pl 
        return [self_pl,alpha]
        
    
    def getInvestHedgeFraction(pl,hedge_attack_power=4,hedge_x_bias=1.0):
        invf = 1.0
        print('getInvestHedgeFraction')
        print('pl ', str(pl))
        print('att ', str(hedge_attack_power))
        print('xb ',  str(hedge_x_bias))
        
        if not pl == None: 
            v = pl
            invf = hedge_x_bias/(v**hedge_attack_power+0.5)
            if invf>1:
                invf = 1.0
        frac_invest = invf
        frac_hedge = 1.0 - invf
        print('results')
        print(str(frac_invest))
        print(str(frac_hedge))
        
        return frac_invest,frac_hedge 

    def logExperimentSignals(api_key,pq,date,eid,data):
        log = {
        'DateTime': date,
        'experiment_id' :eid,
        'data_type' :'experiment_signals',
        'log_key':'experiment_signal_'+str(date)+'_'+eid
        }
        data.update(log)
        q = {'api_key' : api_key,'key_field':'log_key','val':data}
        dat = pq.push_data(q,remote=False)
    
    def adjustTargetHoldingsWithInvestHedgeFractions(pl,target_holds_ratio,hedgesymbol,frac_invest,frac_hedge):
        if not pl == None:
            target_holds_ratio_new = {}
            for k in target_holds_ratio:
                if k == hedgesymbol:
                    target_holds_ratio_new[k] = target_holds_ratio[k]* frac_invest + 1.0*frac_hedge
                else:
                    target_holds_ratio_new[k] = target_holds_ratio[k]* frac_invest + 0.0*frac_hedge
            target_holds_ratio = target_holds_ratio_new
            print('new:')
            print(target_holds_ratio)
        return target_holds_ratio
        
    def do_input(self,feature,context):
        import pprint
        import datetime
        import tracemalloc
        tracemalloc.start()
        import time
        start_time = time.time()
        start_time_total = time.time()
        if not 'lockout_until' in context:
            context['lockout_until'] =  feature['time'] - datetime.timedelta(days=1)
            
        try: 
            a = HourlyRebalance.pq
        except Exception as e:
            print(e)
            HourlyRebalance.pq = PaxFinancialAPI.PaxFinancialAPI(url_version='dev')
            
        mos = MarketOsRunner.GetInstance()
        holds_now = mos.getHoldings()
        nw =   feature['time']
        syms = feature['securities']
        
        
        time_in_num = nw - datetime.timedelta(days=feature['numer_days'])
        time_end_num = nw 
        time_in_denom = nw - datetime.timedelta(days=feature['denom_days'])
        time_end_denom = nw 
        
        feature_flow = {'api_key':feature['api_key'], 
                   'time_in_num':time_in_num,  'time_end_num':time_end_num ,
                   'time_in_denom':time_in_denom,  'time_end_denom':time_end_denom ,
                   'symbols':syms,
                    'std_factor':feature['std_factor'],
                    'buy_low':feature['buy_low'],
                       }
        cash = holds_now['cash']
        
        #print("G Current Execution time is  "+ str(time.time()-start_time))
            
        start_date = nw - datetime.timedelta(hours=feature['pl_start_date_delta_hours'])
        end_date = nw - datetime.timedelta(hours=feature['pl_end_date_delta_hours'])
        start_date_2 = nw - datetime.timedelta(hours=feature['pl2_start_date_delta_hours'])
        end_date_2 = nw - datetime.timedelta(hours=feature['pl2_end_date_delta_hours'])
        
        asdfjewriokjsdjkdsfndsfiuewrkjjkdsfkjsdfajsdamndsafkewrkjsdfkj
        
        pl = None
        pl2 = None
        hedgesymbol = feature['pl_hedge_symbol']
        frac_invest = 1.0
        frac_hedge = 0.0
        start_time = time.time()
        frac_hedge_pl=0.0
        frac_hedge_pl2=0.0
        
        
        
        
        if feature['do_pl_hedge'] == True:
            pl = HourlyRebalance.getSelfPL(HourlyRebalance.pq,feature['api_key'],context['experiment_id'],
                                           start_date,end_date,feature['time'],context,'pl')
            pl2 = HourlyRebalance.getSelfPL(HourlyRebalance.pq,feature['api_key'],context['experiment_id'],
                                           start_date_2,end_date_2,feature['time'],context,'pl2')

            print("Total getSelfPL Execution time is  "+ str(time.time()-start_time))
            start_time = time.time()
            [frac_invest_pl,frac_hedge_pl] = HourlyRebalance.getInvestHedgeFraction(pl,
                                                                              hedge_attack_power=feature['pl_hedge_attack'],
                                                                              hedge_x_bias=feature['pl_hedge_x_bias'])
            [frac_invest_pl2,frac_hedge_pl2] = HourlyRebalance.getInvestHedgeFraction(pl2,
                                                                              hedge_attack_power=feature['pl2_hedge_attack'],
                                                                              hedge_x_bias=feature['pl2_hedge_x_bias'])
            
            frac_hedge = max([frac_hedge_pl,frac_hedge_pl2])
            frac_invest = 1.0 - frac_hedge  
            print("Total getInvestHedgeFraction Execution time is  "+ str(time.time()-start_time))
            start_time = time.time()
        if context['lockout_until'] <  feature['time']:
            if pl > feature['lockout_max'] or pl2 > feature['lockout_max']: #We have recently made 10%. It might be prudent to lock out
                context['lockout_until'] =  feature['time'] + datetime.timedelta(days=feature['lockout_days'])
            if pl < feature['lockout_min'] or pl2 < feature['lockout_min']: #We have recently made 10%. It might be prudent to lock out
                context['lockout_until'] =  feature['time'] + datetime.timedelta(days=feature['lockout_days'])
        lockout_hedge = 0
        if context['lockout_until'] > feature['time']:
            frac_invest = 0.0
            frac_hedge = 1.0
            lockout_hedge =1
        #print("F Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        rawHoldData =  HourlyRebalance.getRawHoldings(HourlyRebalance.pq,feature_flow)
        print("Total getHoldings Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        
        holds = rawHoldData[0]
        num = rawHoldData[1]
        denom = rawHoldData[2]
        
        target_holds_ratio = {} 
        for i,row in holds.iterrows():
            target_holds_ratio[row['Ticker']] = row['raw_holds']
        #print("---------------------------------")
        #print("---------------------------------")
        #print("---------------------------------")
        #print(feature['time'])
        #print(target_holds_ratio)
        print("E Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        target_holds_ratio =  HourlyRebalance.adjustTargetHoldingsWithInvestHedgeFractions(pl,
                                                                           target_holds_ratio,
                                                                           hedgesymbol,
                                                                           frac_invest,
                                                                           frac_hedge)

        #print('new target:')
        #print(target_holds_ratio)
        #print("D Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()

        
        dat = HourlyRebalance.getMarketHoldingsStats()
        holds_ratio = dat['holds_ratio'] 
        holds_value = dat['holds_value'] 
        total_value =  sum(list(holds_value.values()))
        #print('holds now:')
        #print(holds_ratio)
        
        orderDelta = HourlyRebalance.getRatioDeltas(holds_ratio,target_holds_ratio)
        #print("C Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        print(orderDelta)
        orderValue = {}
        orderShares = {}
        delta_abs_sum = 0.0
        for k in orderDelta:
            delta_abs_sum = delta_abs_sum + abs(float(orderDelta[k]))
        
        

        log_data = {'alpha_pl':pl,
                    'frac_invest':frac_invest,
                    'frac_hedge':frac_hedge,
                    'delta_abs_sum':delta_abs_sum,
                    'frac_hedge_pl':frac_hedge_pl,
                    'frac_hedge_pl_2':frac_hedge_pl2,
                    'lockout_hedge':lockout_hedge, 
                    'pl':pl,
                    'pl2':pl2
                   }
        for k in holds_now:
            log_data['hold_'+k] =  holds_now[k]
        for k in holds_value:
            log_data['value_'+k] =  holds_value[k]
        for k in holds_ratio:
            log_data['ratio_'+k] =  holds_ratio[k]
            
        HourlyRebalance.logExperimentSignals(feature['api_key'],
                                             HourlyRebalance.pq,
                                             feature['time'],
                                             context['experiment_id'],
                                             log_data)
        
        
        if delta_abs_sum< feature['rebalance_on_minimum_delta']:
            print('sk sum ',str(delta_abs_sum), ' min ',str(feature['rebalance_on_minimum_delta']))
            print(orderDelta)
            current, peak = tracemalloc.get_traced_memory()
            print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
            print("Total Current Execution time is  "+ str(time.time()-start_time_total))
            tracemalloc.stop()        
            
            return None
        #print("B Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
        
        for k in orderDelta:
            if k != 'cash' and mos.getAsk(k): 
                orderValue[k] = total_value*orderDelta[k]
                orderShares[k] = orderValue[k]/mos.getAsk(k)
            elif  k != 'cash':
                orderValue[k] = None
                orderShares[k] = None
            else:
                orderValue[k] = total_value*orderDelta[k]
                orderShares[k] = orderValue[k]                
        #print("A Current Execution time is  "+ str(time.time()-start_time))
        start_time = time.time()
                
        #print('*')
        #print(orderDelta)
        #print(orderValue)
        #print(orderShares)
        #print('*')
        for sec in orderShares:
            shares =orderShares[sec]
            if sec != 'cash' and shares and mos.getAsk(sec):
                if abs(shares*mos.getAsk(sec)) > 20:
                    mos.order(security=sec,amount=shares)
            if sec == 'cash':
                pass #Taken care of by selling out of other positions in the != cash category
        #mos.order(security,amount,expire_security_value=None,expire_security_holding_rate=None,originalShareValue=None,bracket_order = None):
        # order(self,security,amount,expire_security_value=None,expire_security_holding_rate=None,originalShareValue=None,bracket_order = None):
        # avg_now = mos.get_price_avg(feature,context,start_date,limit_timedelta,target_sec)
        # mos.do_order_bracket(target_sec,
        #                                    testOrder=False,
        #                                    limit_max = bracket_limit_max,
        #                                    limit_min = bracket_limit_min,
        #                                    limit_timedelta=datetime.timedelta(days=bracket_limit_days),
        #                                    trade_size = holds['cash']*invest_fraction, # Grab 10 shares
        #                                    order_type = "buy",
        #                                    )                      
        
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        print("Total Current Execution time is  "+ str(time.time()-start_time_total))
        start_time = time.time()
        tracemalloc.stop()
        
        return None
    
import pprint,json

# Add to PL code - code that estimates value of  PL before data comes in based on avg os securities 
'''
        q = { 'api_key' : api_key,'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        self.assertTrue('experiment_id' in dat, 'Could not start process')
        eid = dat['experiment_id']
        print(eid)
        q = {'api_key':api_key,'query':{'eid':eid}}
        dat = pq.find_processes(q,remote=True)
        # empty dictionary here is ok but not required        
        
    def test_launch_empty_code_string(self):
        minutes=5
        record_steps=0
        min_date = datetime.datetime.utcnow()
        financialNetworkDef,codeString = self.create_realtime_process(minutes,record_steps)
        codeString = ""   
        q = { 'api_key' : api_key,'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True) 
        self.assertTrue('experiment_id' in dat, 'Could not start process')
        eid = dat['experiment_id']
        print(eid)
        q = {'api_key':api_key,'query':{'eid':eid}}
        dat = pq.find_processes(q,remote=True)
        # dat = empty dictionary here is ok but not required

    def test_launch_with_nondict_settings(self):
        minutes=5
        record_steps=0
        min_date = datetime.datetime.utcnow()
        financialNetworkDef,codeString = self.create_realtime_process(minutes,record_steps)  
        q = { 'api_key' : api_key,'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : ['alpha','beta'],'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        print(dat)
        self.assertEqual(len(dat),1, "response should contain 1 field")
        self.assertTrue('error' in dat.keys(),"response dict should contain 'error' field") 
        
        
        
    def test_launch_with_bad_API_key(self):
        minutes=5
        record_steps=0
        min_date = datetime.datetime.utcnow()
        financialNetworkDef,codeString = self.create_realtime_process(minutes,record_steps)
        
        # no API key
        q = {'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        print(dat)
        self.assertEqual(len(dat),1, "response should contain 1 field")
        self.assertTrue('error' in dat.keys(),"response dict should contain 'error' field")   
        
        # API key = None
        q = {'api_key' : None, 'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        print(dat)
        self.assertEqual(len(dat),1, "response should contain 1 field")
        self.assertTrue('error' in dat.keys(),"response dict should contain 'error' field")      
    
        # random API key        
        q = {'api_key' : "pkey-"+str(uuid.uuid1()), 'name_prefix' : 'test_financial_process_simulation','process_settings' : {},
    'launch_settings' : {'mode':'jef'},'network_def' : financialNetworkDef,'code' : codeString,}
        dat = pq.launch_financial_process(q,remote=True)
        print(dat)
        self.assertEqual(len(dat),1, "response should contain 1 field")
        self.assertTrue('error' in dat.keys(),"response dict should contain 'error' field") 
               
        
    def test_halt_process(self,pause=5):
        [status,eid] = TestLaunchFinancialProcess.launch_a_test_process(self,2)
        print(status)
        self.assertEqual(status in ['running'], True, 'Process is not running, status = ' + str(status))        
        pq.halt_process({'api_key':api_key,'experiment_id':eid})    
        time.sleep(pause)
        q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)
        try:
            status = list(pd.DataFrame(dat)['status'])[0]
        except Exception as e:
            print(dat)
            raise e 
        self.assertEqual(status,'halted',"job status should be 'halted'") 
        
    def test_delete_process(self,pause=5):
        #start job running
        [status,eid] = TestLaunchFinancialProcess.launch_a_test_process(self,2)
        print(status)
        self.assertEqual(status,'running', 'Process is not running, status = ' + str(status))
        
        #attempt to delete running process, which should not be possible
        pq.delete_process(q={'api_key':api_key,'experiment_id':eid},remote=True)           
        q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)
        self.assertTrue(len(dat)>0, 'process appears to have been deleted' )
        
        # now we halt process, delete it, and check that get_last_logs returns an empty structure
        pq.halt_process({'api_key':api_key,'experiment_id':eid})    
        time.sleep(pause)
        q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)
        try:
            status = list(pd.DataFrame(dat)['status'])[0]
        except Exception as e:
            print(dat)
            raise e 
        self.assertEqual(status,'halted',"job status should be 'halted'")
        pq.delete_process(q={'api_key':api_key,'experiment_id':eid},remote=True)           
        q = { 'api_key' : api_key,'query':{'experiment_id':eid}}
        dat = pq.find_processes(q,remote=True)
        self.assertEqual(len(dat),0, 'process could not be deleted' ) 
        dat = pq.get_last_logs( {'api_key':api_key,'experiment_id':eid}, remote=True )
        self.assertEqual(len(dat),0, 'last logs from deleted process should be empty' ) 
  
        
    def test_get_last_logs(self):
        #start a job, check that we can get its last logs
        [status,eid] = TestLaunchFinancialProcess.launch_a_test_process(self,2)
        print(status)
        self.assertEqual(status,'running', 'Process is not running, status = ' + str(status))        
        dat = pq.get_last_logs( {'api_key':api_key,'experiment_id':eid}, remote=True )
        self.assertTrue(len(dat)>0, 'last logs from running process are empty' )
  
    def test_get_last_logs_nonexistent_process(self):
        #attempt to get last logs from a nonexistent job
        eid = uuid.uuid1()   # since this is a unique id, no experiment should have it as an id
        dat = pq.get_last_logs( {'api_key':api_key,'experiment_id':eid}, remote=True )
        print(dat)
        self.assertEqual(len(dat),0, 'last logs from nonexistent experiment should be empty' ) 
        
    
        
        
        
if __name__ == '__main__':
    unittest.main()