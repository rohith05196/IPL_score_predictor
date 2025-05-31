from flask import Flask, request, render_template
import pickle
import numpy as np

model = pickle.load(open('ipl_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    batting_team = request.form['batting-team']
    bowling_team = request.form['bowling-team']
    overs = float(request.form['overs'])
    runs = int(request.form['runs'])
    wickets = int(request.form['wickets'])
    runs_last_5 = int(request.form['runs-last-5'])
    wickets_last_5 = int(request.form['wickets-last-5'])

    # Create a dictionary mapping teams to their one-hot vectors
    teams = [
        'Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders',
        'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
        'Royal Challengers Bengaluru', 'Sunrisers Hyderabad'
    ]

    # Create the one-hot encoding dictionary
    team_encoding = {team: [i == idx for i in range(len(teams))] for idx, team in enumerate(teams)}

    # Initialize the temp_arr with the input features
    temp_arr = [runs, wickets, overs, runs_last_5, wickets_last_5]

    # Encode batting team
    batting_vector = team_encoding.get(batting_team)
    if not batting_vector:
        return "Invalid batting team"
    temp_arr += batting_vector

    # Encode bowling team
    bowling_vector = team_encoding.get(bowling_team)
    if not bowling_vector:
        return "Invalid bowling team"
    temp_arr += bowling_vector

    # temp_arr now has the features followed by one-hot encodings for both teams


    prediction = model.predict(np.array([temp_arr]))

    score = int(prediction[0])
    max_score = score+5
    min_score = score-5
    return render_template('index.html', prediction_text=f'{min_score} to {max_score} runs')


if __name__ == "__main__":
    app.run(debug=True)
