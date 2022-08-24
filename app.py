import json
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#----------------------------------------#
# Database Setup
#----------------------------------------#
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)
station = Base.classes.station
measurement = Base.classes.measurement

#----------------------------------------#
# Flask Setup
#----------------------------------------#
app = Flask(__name__)

#----------------------------------------#
# Flask Routes
#----------------------------------------#

# Initial Homepage that displays all of
# of the available routes.
#-----------------------------------------
@app.route("/")
def home():
    print("Home")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start: yyyy-mm-dd]<date:start><br/>"
        f"/api/v1.0/[start: yyyy-mm-dd]<start>/[end: yyyy-mm-dd]<end><br/>"
    )

# Displays the dates and precipitation of
# all query results as a dictionary.
#-----------------------------------------
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Precipitation")

    # Query to retrieve data and precipitation scores of all results
    # and populate the results into a dateframe
    sqlDF = pd.read_sql(
    f'SELECT date,prcp FROM measurement',
    con=engine,
    )

    sqlDF = sqlDF.set_index('date') # Sets date as index column
    sqlDF = sqlDF.dropna() # Drops rows with N/A values

    prcpDict = {}

    # Populates results into a dictionary
    for row,value in sqlDF.iterrows():
        prcpDict[row] = value["prcp"]

    return jsonify(prcpDict)

# Displays a list of all unique stations
# from the station table.
#-----------------------------------------
@app.route("/api/v1.0/stations")
def stations():
    print("Stations")
    session = Session(engine) # Starts session

    # Query to pull the station column for all stations in
    # the station table
    results = session.query(station.station).all()

    session.close() # Closes session

    # Converts results to a list
    allStations = list(np.ravel(results))

    return jsonify(allStations)

# Displays list of temperatures for the
# past year for the most active station
# : USC00519281
#-----------------------------------------
@app.route("/api/v1.0/tobs")
def tobs():
    print("Temperature Observations")
    session = Session(engine) # Starts session

    # Query to find the most active stations based on number of rows for each station
    # sorting by descending order.
    activeStationQuery = session.query(measurement.station, func.count(measurement.station)). \
                        group_by(measurement.station). \
                        order_by(func.count(measurement.station).desc()). \
                        all()

    mostActiveStation = activeStationQuery[0][0] # Takes the first station in the sorted list
    print(f"Active Station: {mostActiveStation}")

    # Query to find the date of the first result for the most active station
    firstRow = session.query(measurement).filter_by(station=f'{mostActiveStation}').first()
    activeStationRecentDate = firstRow.date

    # Loop through query results to identify the most recent date of the most active station
    for row in session.query(measurement.date).filter_by(station=f'{mostActiveStation}').all():
        currentDate = row.date
        if currentDate > activeStationRecentDate:
            activeStationRecentDate = currentDate

    # Calculates the year prior to the most recent date
    activeStationYearPrior = str(dt.date(int(activeStationRecentDate[:4]), int(activeStationRecentDate[5:7]), int(activeStationRecentDate[-2:])) - dt.timedelta(days=365))

    # Query to identify the temperatures of the most active station for 
    # the previous year and populate the results into a dataframe
    activeStationTobsDF = pd.read_sql(
        f'SELECT date,tobs FROM measurement WHERE date > "{activeStationYearPrior}" AND station = "{mostActiveStation}"',
        con=engine,
    )

    session.close() # Closes session
    activeStationTobsDF = activeStationTobsDF.dropna() # Drops rows with NA values

    # Converts temperature results to a list
    allTobs = list(np.ravel(activeStationTobsDF['tobs']))

    return jsonify(allTobs)

# Calculates the min, max, and avg of
# temperatures starting at a given date to
# the end of the dataset.
#-----------------------------------------
@app.route("/api/v1.0/<start>")
def start(start):
    print("Start Date")
    session = Session(engine) # Starts session

    # Query to calculate the min, max, and age starting at the
    # provided date in the parameter to the end date of the dataset
    results = session.query(func.min(measurement.tobs), \
                                       func.max(measurement.tobs), \
                                       func.avg(measurement.tobs)). \
                        filter(measurement.date >= start).all()

    session.close() # Closes session

    # Converts temperature results to a list
    startList = list(np.ravel(results))

    return jsonify(startList)

# Calculates the min, max, and avg of
# temperatures starting at a given date to
# a given end date.
#-----------------------------------------
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    print("Start Date")
    session = Session(engine) # Starts session

    # Checks if the end date is greater than the start date to
    # ultimately validate that the end date is after the start date
    if end > start: 
        results = session.query(func.min(measurement.tobs), \
                                        func.max(measurement.tobs), \
                                        func.avg(measurement.tobs)). \
                            filter(measurement.date >= start, measurement.date <= end).all()

        session.close() # Closes session

        # Converts temperature results to a list
        startEndList = list(np.ravel(results))

        return jsonify(startEndList)
    else: # Return an error message if the date is not after the start date
        return jsonify({"error": f"End date {end} is not after {start}"}), 404

# Runs the Flask app
if __name__ == "__main__":
    app.run(debug=True)