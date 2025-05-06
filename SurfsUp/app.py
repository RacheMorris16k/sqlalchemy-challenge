# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine(r"sqlite:///C:\Users\rache\sqlalchemy-challenge\Resources\hawaii.sqlite")

# reflect the tables
Base = automap_base()

# Save references to each table
Base.prepare(autoload_with=engine)

# Create our session (link) from Python to the DB
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precip_dict = {date: prcp for date, prcp in data}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    station_list = [s[0] for s in results]
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = [t[0] for t in results]
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temps = list(results[0])
    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)