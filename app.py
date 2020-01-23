import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    "Available Routes."
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    "Return the JSON representation of your dictionary."

    precip_data = Session.query(Measurement.date, Measurement.prcp).filter(Measurement.data.between('2016-08-23', '2017-08-23')).all()

    precipitation = []
    for precip in precip_data:
        row = {"date":"prcp"}
        row["date"] = precip[0]
        row["prcp"] = precip[1]
        precipitation.append(row)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    "Return a JSON list of stations from the dataset."

    station_data = session.query(Station.station, Station.station_name).group_by(Station.station).all()
    station_list = list(station.results)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    "Return a JSON list of Temperature Observations (tobs) for the previous year."

    tobs_data = session.query(Measurement.station, Measurement.tobs).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()
    tobs_list = []
    for tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["station"] = tobs[0]
        tobs_dict["tobs"] = tobs[1]
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def calc_temps(start='start_date'):
    start_date = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
    start_data = Session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date)

    start_tobs = []
    for tobs in start_data:
        tobs_dict = {}
        tobs_dict["TAVG"] = tobs[2]
        tobs_dict["TMAX"] = tobs[0]
        tobs_dict["TMIN"] = tobs[1]

        start_tobs.append(tobs_dict)

    return jsonify(start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def calc_temps_2(start="start_date", end="end_date"):
    start = datetime.strptime('2016-08-23', '%Y-%m-%d').date()
    end = datetime.strptime('2017-08-23', '%Y-%m-%d').date()

    total = session.query(func.max(Measurement.tobs).label("max_tobs"), func.min(Measurement.tobs).label("min_tobs"), func.avg(Measurement.tobs).label("avg_tobs")).filter(Measurement.date.between(start_date, end_date))

    total_tobs = []
    for tobs in total:
        tobs_dict = {}
        tobs_dict["TAVG"] = tobs[2]
        tobs_dict["TMAX"] = tobs[0]
        tobs_dict["TMIN"] = tobs[1]

        total_tobs.append(tobs_dict)
    
    return jsonify(total_tobs)

if __name__ == '__main__':
    app.run(debug=True)

