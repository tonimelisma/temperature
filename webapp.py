#!/usr/bin/python3
#
# Copyright (c) Toni Melisma 2022

import time
from flask import Flask, Response, render_template, jsonify
import weathermodel
from meteocalc import Temp, feels_like

app = Flask(__name__)


@app.route("/ping")
def ping_handler():
    return Response("pong", mimetype="text/plain")


@app.route("/")
def index_handler():
    start_time = time.time()

    latest_measurement = weathermodel.select_latest_measurement()
    print(f"Time after select_latest_measurement: {time.time() - start_time}s")

    if latest_measurement.pressure < 1009.1:
        pressure_classification = "low"
    elif latest_measurement.pressure > 1009.1 and latest_measurement.pressure < 1022.7:
        pressure_classification = "medium"
    else:  # latest_measurement.pressure > 1022.7:
        pressure_classification = "high"
    this_temperature = Temp(latest_measurement.temperature, "c")

    print(
        f"Time after pressure classification and temperature calculation: {time.time() - start_time}s")

    latest_windspeed = weathermodel.calculate_latest_average_windspeed()
    print(
        f"Time after calculate_latest_average_windspeed: {time.time() - start_time}s")

    feels_like_temperature = feels_like(
        temperature=this_temperature, humidity=latest_measurement.humidity, wind_speed=latest_windspeed)
    print(f"Time after feels_like calculation: {time.time() - start_time}s")

    print(f"Total execution time: {time.time() - start_time}s")

    return render_template("index.html", temperature_celsius=latest_measurement.temperature, temperature_fahrenheit=this_temperature.f, heat_index_celsius=feels_like_temperature.c, heat_index_fahrenheit=feels_like_temperature.f, pressure=latest_measurement.pressure, pressure_classification=pressure_classification, humidity=latest_measurement.humidity, timestamp=latest_measurement.timestamp)


@app.route("/last7days")
def last7days_handler():
    start_time = time.time()

    measurements = weathermodel.select_last7days_measurements()
    print(
        f"Time after select_last7days_measurements: {time.time() - start_time}s")

    list = []
    for thisrow in measurements:
        list.append({"timestamp": thisrow.timestamp, "temperature": thisrow.temperature,
                    "pressure": thisrow.pressure, "humidity": thisrow.humidity})

    print(f"Total execution time: {time.time() - start_time}s")

    return (jsonify(list))
