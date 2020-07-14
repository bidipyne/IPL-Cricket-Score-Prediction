from flask import Flask, jsonify, request, render_template
import util
import sys
import logging
import json

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/', methods=['GET'])
def home():
    return render_template('app.html')

@app.route('/venue', methods=['GET'])
def get_venue_list():
    if request.method == 'GET':
        venue_list = util.venue_list()
        app.logger.info('venue_list....'+" ".join(venue_list))
        venue_list = [each.title() for each in venue_list]
        response = json.dumps(venue_list, indent=2)
        #response = jsonify({ 'venue' : venue_list })
        #response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/batting', methods=['GET'])
def get_batting_list():
    if request.method == 'GET':
        batting_list = util.batting_team()
        batting_list = [each.replace('bat_team_', '').title() for each in batting_list]
        response = json.dumps(batting_list, indent=2)
        return response

@app.route('/bowling', methods=['GET'])
def get_bowling_list():
    if request.method == 'GET':
        bowling_list = util.bowling_team()
        bowling_list = [each.replace('bowl_team_', '').title() for each in bowling_list]
        response = json.dumps(bowling_list, indent=2)
        return response

@app.route('/predict', methods=['POST'])
def predict():
    batting = request.form['batting']
    bowling = request.form['bowling']
    venue =  request.form['venue']
    overs = float(request.form['overs'])
    runs = int(request.form['runs'])
    wickets = int(request.form['wickets'])
    pruns = int(request.form['pruns'])
    pwickets = int(request.form['pwickets'])

    output = util.score_estimation(runs, wickets, overs, pruns, pwickets, venue, batting, bowling)
    return render_template('app.html', predicted_score="Predicted score {}".format(output))
    #return response


if __name__=='__main__':
    util.load_artifacts()
    print('Server started running....')
    app.logger.info('Server started running....')
    app.run(debug=True)

