import json
import pickle
import numpy as np

__data_columns = None
__venue = None
__bat_team = None
__bowl_team = None
__batsman = None
__bowler = None
__model = None
__stddev = None

def venue_list():
    return __venue

def batting_team():
    return __bat_team

def bowling_team():
    return __bowl_team

def get_batsman():
    return __batsman

def get_bowler():
    return __bowler

def standard_deviation():
    return __stddev

def load_artifacts():
    print('*****Loading Artifacts Started*****')
    global __data_columns
    global __venue
    global __bat_team
    global __bowl_team
    global __batsman
    global __bowler
    global __stddev
    with open('columns.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __batsman = __data_columns[5:36]
        __bowler = __data_columns[36:60]
        __venue = __data_columns[60:71]
        __bat_team = __data_columns[71:78]
        __bowl_team = __data_columns[78:]

    with open('columns.json', 'r') as f:
        __stddev = json.load(f)['stddev']

    global __model
    with open('./first-innings-score-lasso-model.pkl', 'rb') as fp:
        __model = pickle.load(fp)
    print('****Artifacts Loaded Successfully****')
    
def score_estimation(runs, wickets, overs, pruns, pwickets, batsman, bowler, venue, batting, bowling):
    batsman_index = __data_columns.index(batsman.lower()+' batsman')
    bowler_index = __data_columns.index(bowler.lower()+' bowler')
    venue_index = __data_columns.index(venue.lower())
    batting_index = __data_columns.index('bat_team_'+batting.lower())
    bowling_index = __data_columns.index('bowl_team_'+bowling.lower())
    
    x  = np.zeros(len(__data_columns))
    x[0] = runs
    x[1] = wickets
    x[2] = overs
    x[3] = pruns
    x[4] = pwickets
    if batsman_index > 0 :
        x[batsman_index] = 1
    if bowler_index > 0 :
        x[bowler_index] = 1
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