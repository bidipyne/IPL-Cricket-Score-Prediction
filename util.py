import json
import pickle
import numpy as np

__data_columns = None
__venue = None
__bat_team = None
__bowl_team = None
__model = None
__stddev = None

def venue_list():
    return __venue

def batting_team():
    return __bat_team

def bowling_team():
    return __bowl_team

def standard_deviation():
    return __stddev

def load_artifacts():
    print('*****Loading Artifacts Started*****')
    global __data_columns
    global __venue
    global __bat_team
    global __bowl_team
    global __stddev
    with open('columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __venue = __data_columns[5:16]
        __bat_team = __data_columns[16:24]
        __bowl_team = __data_columns[24:32]

    with open('columns.json', 'r') as f:
        __stddev = json.load(f)['stddev']

    global __model
    with open('./first-innings-score-lasso-model.pkl', 'rb') as fp:
        __model = pickle.load(fp)
    print('****Artifacts Loaded Successfully****')
    
def score_estimation(runs, wickets, overs, pruns, pwickets,venue, batting, bowling):
    venue_index = __data_columns.index(venue.lower())
    batting_index = __data_columns.index('bat_team_'+batting.lower())
    bowling_index = __data_columns.index('bowl_team_'+bowling.lower())
    
    x  = np.zeros(len(__data_columns))
    x[0] = runs
    x[1] = wickets
    x[2] = overs
    x[3] = pruns
    x[4] = pwickets
    if venue_index > 0 :
        x[venue_index] = 1
    if batting_index > 0 :
        x[batting_index] = 1
    if bowling_index > 0 :
        x[bowling_index] = 1
        
    return int(__model.predict([x])[0])
    
if __name__=='__main__':
    load_artifacts()
    print('Server started running....')
    #app.run()