# data_flask_api

### Intro
This Flask app will create an API interface for the Data Teams solutions for ["The Bridge" bootcamp final project](https://www.thebridge.tech/blog/reto-de-tripulaciones-the-bridge) (gtT-HIV e-learning platform). This project gives is a cross vertical team (FS, cybersecurity, marketing, UX and data) just under two weeks to develop a MVP for an e-learning platform for the organisation [gTt-HIV](http://www.gtt-vih.org/).

### Our solutions
Our solutions include content recommendation models, predictive models of user engagement/abandonment as well as a live dashboard for admin to get insights about the consumption of content on their e-learning platform. 

#### Recommendation model (`/recom`)
Implemented as an API endpoint where two parameters (user_id and course_id) are used. The API loads in the "consumption table" from the elephantSQL database and creates a cosine distance matrix on the courses based on user consumption patterns. For a given user and a given course, the model returns 3 other courses (that the user in question has not accessed) in JSON format for intergration with the front-end course page.

example url: 

`/recom?user_id=4&course_id=5`

returns: 

`{
  "course_ids": [
    13,
    33,
    1
  ]
}`


#### Course Abandonment Prediction (`/retrain_abandon` & `/predict_abandon`)
This uses a classification model to predict abandonment or not of any course for a given user. Abandonment is defined with a cutoff for inactivity (time since log course material access) on a given course. One endpoint allows the retraining of the model on the latest postgreSQL data which saves the pipeline (standard scaler and random forest classifier). The other endpoint is designed to be used by the streamlit dashboard where a user_id is sent, the data for that user is pulled from the DB, processed and the pipeline is used to make a prediction which is returned as a JSON file.

example url for prediction:

`/predict_abandon?user_id=11`

returns:

`{
  "Prediction": "not_abandon"
}`


