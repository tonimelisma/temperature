#!/usr/bin/python3
#
# Copyright (c) Toni Melisma 2022

import weathermodel
import smbus2
import bme280
from datetime import datetime
from dateutil import tz
import logging

port = 1
address = 0x77
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)
weathermodel.initialize()

data = bme280.sample(bus, address, calibration_params)

#print(type(data.id), ":", data.id)
#print(type(data.timestamp), ":", data.timestamp)
#print(type(data.temperature), ":", data.temperature)
#print(type(data.pressure), ":", data.pressure)
#print(type(data.humidity), ":", data.humidity)

transformed_id = str(data.id)
local_timezone = tz.tzlocal()
transformed_timestamp = data.timestamp.astimezone(local_timezone)

this_measurement = weathermodel.Measurement(
    id=transformed_id,
    timestamp=transformed_timestamp,
    temperature=data.temperature,
    pressure=data.pressure,
    humidity=data.humidity)

weathermodel.insert_measurement(this_measurement)
