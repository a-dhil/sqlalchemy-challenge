# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
from datetime import datetime, timedelta
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base=automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################

app=Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Honolulu, Hawaii Climate Data API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date_str=recent_date[0]
    most_recent_date=dt.datetime.strptime(most_recent_date_str,'%Y-%m-%d')
    year_ago=most_recent_date - dt.timedelta(days=366)
    results=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date>=year_ago).\
    filter(Measurement.date<=most_recent_date).all()
      # Convert results into dictionary
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp 
        
    #Return JSON representation of data
    session.close()
    return jsonify(precipitation_data)



@app.route("/api/v1.0/stations")

def station():
    #active_stations = session.query(Measurement.station, func.count(Measurement.station).label('count')).\
    #group_by(Measurement.station).\
    #order_by(func.count(Measurement.station).desc()).all()
    stations=session.query(Station.station).all()
    
    # Convert the data to a Python list of dictionaries
    station_list = [{'station': station[0]} for station in stations]
    session.close()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")

def tobs():
    recent_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    most_recent_date_str=recent_date[0]
    active_stations = session.query(Measurement.station, func.count(Measurement.station).label('count')).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
    active_station_query=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                    filter(Measurement.station == 'USC00519281').first()
    most_active_station_code = active_stations[0][0]

    # get most recent date 
    most_recent_date_station = session.query(func.max(Measurement.date)).first()
    # get the date as string
    most_recent_date_station_str = most_recent_date_station[0]
    # convert as date object
    most_recent_date_station=dt.datetime.strptime(most_recent_date_str,'%Y-%m-%d')
    # calculate the date one year ago from most recent date given 2016 was leap year
    one_year_ago_station=most_recent_date_station - dt.timedelta(days=366)

    # query the TOBS data
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == most_active_station_code).\
    filter(Measurement.date >= one_year_ago_station).\
    order_by(Measurement.date).all()
    
    tobs_list = [(date, tobs) for date, tobs in tobs_data]
    session.close()
    return jsonify(tobs_list)




@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def statistics(start, end=None):
    # Convert to datetime objects
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    
    if end:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d")
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
            .filter(Measurement.date >= start_date).all()

    # Unpack the results
    if results:
        (min_temp, avg_temp, max_temp) = results[0]
    else:
        min_temp, avg_temp, max_temp = None, None, None

    # Create a dictionary of results
    stats_data = {
        "TMIN": min_temp,
        "TAVG": avg_temp,
        "TMAX": max_temp
    }

    # Return JSON
    session.close()  
    return jsonify(stats_data)

if __name__ == '__main__':
    app.run() 