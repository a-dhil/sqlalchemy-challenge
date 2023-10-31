# sqlalchemy-challenge
GitHub Repo Link: https://github.com/a-dhil/sqlalchemy-challenge
Folder name SurfsUp which has app.py file with code for flask framework app, climate_starter.ipynb file contains the code for analysis and the Resource folder has the data used for this challenge.

# About Challenge

In this asignment, climate analysis was performed on Honolulu, Hawaii dataset.
Tool used to do the basic climate analysis and data exploration of climate database  were Python and SQLAlchemy specifically ORM queries and Matplotlib for charts.

This challenge was divided into two parts:
Part 1
In this section Precipitation Analysis and Station Analysis  was performed using ORM in SQLALchemy.
Part 2
Here basic Climate App was designed from the initial Analysis. The app was constructed usinf Flask framework and creating routes.

# Usage

Part 1

climate_starter.ipynb is a jupyter notebook file the code can be run directly to see the analysis.

Part 2

Run app.py in terminal and then there will be a link "http://127.0.0.1:5000" it will take the user to webpage.
The web page looks as follow:
Welcome to the Honolulu, Hawaii Climate Data API!
Available Routes:
/api/v1.0/precipitation
/api/v1.0/stations
/api/v1.0/tobs
/api/v1.0/
/api/v1.0//

Copy and paste the routes after the link and see the results. 
Make sure to enter dates(%Y-%m-%d)  after /api/v1.0/start date and /api/v1.0/start_date/end_date

# Acknowledgments

In completeing this assignment  Learing Assiatance, Lecture Recordings by our Instructor, my classmate and ChatGPT were helpful. 