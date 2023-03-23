# data_flask_api

### Intro
This Flask app will create an API interface for the Data Teams solutions for ["The Bridge" bootcamp final project](https://www.thebridge.tech/blog/reto-de-tripulaciones-the-bridge) (gtT-HIV e-learning platform). This project gives is a cross vertical team (FS, cybersecurity, marketing, UX and data) just under two weeks to develop a MVP for an e-learning platform for the organisation [gTt-HIV](http://www.gtt-vih.org/).

### Our solutions
Our solutions include content recommendation models, predictive models of user engagement/abandonment as well as a live dashboard for admin to get insights about the consumption of content on their e-learning platform. 

#### Recommendation model
Implemented as an API endpoint where two parameters (user_id and course_id) are posted. The API loads in the "consumption table" from the elephantSQL database and creates a cosine distance matrix on the courses based on user consumption patterns. For a given user and a given course, the model returns 3 other courses (that the user in question has not accessed) in JSON format for intergration with the front-end course page.


