# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify




#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    one_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    new_data = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= one_year_before).all()

    session.close()

    precipitation = {date:prcp for date,prcp in new_data}

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_name = session.query(measurement.station).\
    group_by(measurement.station).all()

    session.close()

    all_stations = list(np.ravel(station_name))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    one_year_before = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    q_tobs = session.query(measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= one_year_before).all()

    session.close()

    qt = list(np.ravel(q_tobs))

    return jsonify(qt)

@app.route("/api/v1.0/temp/<start>")
def start(start):

    session = Session(engine)

    temp_start = session.query(func.max(measurement.tobs), func.avg(measurement.tobs), func.min(measurement.tobs)).\
    filter(measurement.date >= start).all()

    session.close()

    ts = list(np.ravel(temp_start))

    return jsonify(ts)

@app.route("/api/v1.0/temp/<start>/<end>")
def end(start, end):

    session = Session(engine)

    temp_end = session.query(func.max(measurement.tobs), func.avg(measurement.tobs), func.min(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()

    session.close()

    te = list(np.ravel(temp_end))

    return jsonify(te)

if __name__ == '__main__':
    app.run(debug=True)