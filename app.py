from flask import Flask, render_template, request, jsonify
import os, pickle, json, sys
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
import pandas as pd

set_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(set_dir)
sys.path.append('src')

import recommendations
import course_abandon_prediction
import predict_preproc


app = Flask(__name__, template_folder = 'templates/')
app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recom', methods = ['GET'])
def get_recomendations():
    args = request.args.to_dict()
    user_id = int(args.get("user_id"))
    course_id = int(args.get("course_id"))

    # read in the "consumption" table from elephant SQL
    long_df = recommendations.consumption_to_df()
    # convert to wide format
    wide_df = recommendations.convert_long_to_wide_df(long_df)
    # create the cosine distance matrix
    cos_sim_mat = recommendations.make_cosine_sim_matrix(wide_df)
    # now get the index of the content/course in question
    content_index = recommendations.get_content_index(wide_df, course_id)
    # get the list of indices for courses already viewed by user
    already_seen = recommendations.check_already_seen(user_id, wide_df)
    # now get the 3 closest recommendations
    recom_json = recommendations.find_closest_content(cos_sim_mat, content_index, already_seen, 3)
    
    return recom_json


@app.route('/retrain_abandon', methods = ['POST'])
def retrain():

    X, y, _ = course_abandon_prediction.create_data_aban_model()

    pipe = Pipeline([
        ('scaler', StandardScaler()), 
        ('rfc', RandomForestClassifier(random_state = 17, n_estimators = 51, max_depth = 3))])

    pipe.fit(X.values, y)

    with open('model/model_pipe.pkl', 'wb') as f:
        pickle.dump(pipe, f)

    return 'Model Retrained'



@app.route('/predict_abandon', methods=['GET'])
def predict():
    args = request.args.to_dict()
    user_id = int(args.get("user_id"))

    df = predict_preproc.return_for_predict(user_id)

    model = pickle.load(open('model/model_pipe.pkl', 'rb'))

    prediction = model.predict(df.values)
    mapping = {
        0: 'not_abandon',
        1: 'will_abandon'}
    
    prediction_str = mapping[prediction[0]]

    return jsonify({'Prediction': prediction_str})


if __name__ == "__main__":
    app.run(host = 'localhost', port = 5000, debug = True)