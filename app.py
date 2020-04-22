import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#-----------------Setting up the database------------------
engine = create_engine("sqlite:///hawaii.sqlite")

#----------------Reflect the database------------------------
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#------------------Creating the session----------------------
session = Session(engine)

#----------------Creating the app----------------------------
app = Flask(__name__)

#--------------------Flask Routes----------------------------
@app.route("/")
def home():
    """List all available api routes"""
    return(
        f""
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    one_year_ago = dt.datetime.strptime(last_date,"%Y-%m-%d") - dt.timedelta(days=365)
    data_precp_score = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >=one_year_ago).all()
    data = {date: prcp for date, prcp in data_precp_score}
    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    stations = list(np.ravel(most_active_stations))
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'tobs' page...")
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    most_station_temps = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    most_station_temps = most_station_temps[0]
    one_year_ago = dt.datetime.strptime(last_date,"%Y-%m-%d") - dt.timedelta(days=365)
    temp_observations = session.query(Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == most_station_temps).all()
    data = {date: tobs for date, prcp in temp_observations}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)

