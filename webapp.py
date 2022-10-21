#!/usr/bin/python3
#
# Copyright (c) Toni Melisma 2022

from flask import Flask, Response, render_template, jsonify
import weathermodel
from meteocalc import Temp, feels_like

app = Flask(__name__)


@app.route("/ping")
def ping_handler():
    return Response("pong", mimetype="text/plain")


@app.route("/")
def index_handler():
    latest_measurement = weathermodel.select_latest_measurement()
    if latest_measurement.pressure < 1009.1:
        pressure_classification = "low"
    elif latest_measurement.pressure > 1009.1 and latest_measurement.pressure < 1022.7:
        pressure_classification = "medium"
    else:  # latest_measurement.pressure > 1022.7:
        pressure_classification = "high"
    this_temperature = Temp(latest_measurement.temperature, "c")

    latest_windspeed = weathermodel.calculate_latest_average_windspeed()

    #this_heat_index = heat_index(temperature=this_temperature, humidity=latest_measurement.humidity)
    feels_like_temperature = feels_like(
        temperature=this_temperature, humidity=latest_measurement.humidity, wind_speed=latest_windspeed)

    return render_template("index.html", temperature_celsius=latest_measurement.temperature, temperature_fahrenheit=this_temperature.f, heat_index_celsius=feels_like_temperature.c, heat_index_fahrenheit=feels_like_temperature.f, pressure=latest_measurement.pressure, pressure_classification=pressure_classification, humidity=latest_measurement.humidity, timestamp=latest_measurement.timestamp)


@app.route("/last7days")
def last7days_handler():
    measurements = weathermodel.select_last7days_measurements()
    list = []
    for thisrow in measurements:
        list.append({"timestamp": thisrow.timestamp, "temperature": thisrow.temperature,
                    "pressure": thisrow.pressure, "humidity": thisrow.humidity})
    return (jsonify(list))
