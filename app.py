#########################################################

from flask import Flask, jsonify
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
app = Flask(__name__)

##################Database##############################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base() 
base.prepare(engine, reflect = True)
meas = base.classes.measurement
station = base.classes.station
sess = Session(engine)

#################Flask Routes##########################

@app.route("/")
def home():
    return (
        f"Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<start>/<end> <br/>"
    )


@app.route("/api/v1.0/stations")
def stations():
    sess.query(meas.station).distinct().count()
    active_stations = sess.query(meas.station, func.count(meas.station)).\
        group_by(meas.station).\
        order_by(func.count(meas.station).desc()).all()
    
    
    return jsonify(dict(active_stations))


@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    highest_temp_obs = sess.query(meas.tobs).\
        filter(meas.date >= last_year, meas.station == 'USC00519281').\
        order_by(highest_temp_obs).all()
    
    
    return jsonify(highest_temp_obs)


@app.route("/api/v1.0/<start>")
def start():
    lha_temp = sess.query(func.min(meas.tobs),func.max(meas.tobs),func.avg(meas.tobs)).\
        filter(meas.station == 'USC00519281').order_by(func.min(meas.tobs)).all()
    
    return jsonify(lha_temp)
#########################################################
if __name__ == "__main__":
    app.run(debug=True)
#########################################################