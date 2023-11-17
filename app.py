# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    session.close()

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_name = session.query(measurement.station).\
    group_by(measurement.station).all()

    session.close()

    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    session.close()

@app.route("/api/v1.0/<start>")
def start():

@app.route("/api/v1.0/<start>/<end>")
def end():

if __name__ == '__main__':
    app.run(debug=True)