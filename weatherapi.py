#!/usr/bin/python3
#
# Copyright (c) Toni Melisma 2022

import weathermodel
import requests
from datetime import datetime
import uuid

from meteocalc import Temp

import config


def get_openweathermap():
    response = requests.get(config.OPENWEATHERMAP_URL)
    current_conditions = response.json()
    model_current_conditions = weathermodel.APICurrentCondition()
    model_current_conditions.id = str(uuid.uuid4())
    if current_conditions["weather"][0]["main"]:
        model_current_conditions.weather_condition = current_conditions["weather"][0]["main"]
    if current_conditions["main"]["temp"]:
        tmp_temperature = Temp(current_conditions["main"]["temp"], "k")
        model_current_conditions.temperature = float(tmp_temperature.c)
    if current_conditions["main"]["feels_like"]:
        tmp_feels_like = Temp(current_conditions["main"]["feels_like"], "k")
        model_current_conditions.feels_like_temperature = float(
            tmp_feels_like.c)
    if current_conditions["main"]["pressure"]:
        model_current_conditions.pressure = current_conditions["main"]["pressure"]
    if current_conditions["main"]["humidity"]:
        model_current_conditions.humidity = current_conditions["main"]["humidity"]
    if current_conditions["visibility"]:
        model_current_conditions.visibility = current_conditions["visibility"]
    if current_conditions["wind"]["speed"]:
        model_current_conditions.wind_speed = current_conditions["wind"]["speed"]
    if current_conditions["wind"]["gust"]:
        model_current_conditions.wind_gust = current_conditions["wind"]["gust"]
    if current_conditions["clouds"]["all"]:
        model_current_conditions.cloudiness = current_conditions["clouds"]["all"]
    if current_conditions["dt"]:
        model_current_conditions.timestamp = datetime.fromtimestamp(
            current_conditions["dt"])
    model_current_conditions.data_source = "openweathermap"
    weathermodel.insert_api_current_condition(model_current_conditions)


def get_accuweather():
    response = requests.get(config.ACCUWEATHER_URL)
    current_conditions = response.json()
    model_current_conditions = weathermodel.APICurrentCondition()
    model_current_conditions.id = str(uuid.uuid4())
    if current_conditions[0]["WeatherText"]:
        model_current_conditions.weather_condition = current_conditions[0]["WeatherText"]
    if current_conditions[0]["Temperature"]["Metric"]["Value"]:
        model_current_conditions.temperature = current_conditions[
            0]["Temperature"]["Metric"]["Value"]
    if current_conditions[0]["RealFeelTemperature"]["Metric"]["Value"]:
        model_current_conditions.feels_like_temperature = current_conditions[
            0]["RealFeelTemperature"]["Metric"]["Value"]
    if current_conditions[0]["RealFeelTemperatureShade"]["Metric"]["Value"]:
        model_current_conditions.feels_like_shade_temperature = current_conditions[
            0]["RealFeelTemperatureShade"]["Metric"]["Value"]
    if current_conditions[0]["RelativeHumidity"]:
        model_current_conditions.humidity = current_conditions[0]["RelativeHumidity"]
    if current_conditions[0]["Wind"]["Speed"]["Imperial"]["Value"]:
        model_current_conditions.wind_speed = current_conditions[
            0]["Wind"]["Speed"]["Imperial"]["Value"]
    if current_conditions[0]["WindGust"]["Speed"]["Imperial"]["Value"]:
        model_current_conditions.wind_gust_speed = current_conditions[
            0]["WindGust"]["Speed"]["Imperial"]["Value"]
    if current_conditions[0]["UVIndex"]:
        model_current_conditions.uv_index = current_conditions[0]["UVIndex"]
    if current_conditions[0]["Visibility"]["Metric"]["Value"]:
        model_current_conditions.visibility = current_conditions[
            0]["Visibility"]["Metric"]["Value"]*1000
    if current_conditions[0]["CloudCover"]:
        model_current_conditions.cloudiness = current_conditions[0]["CloudCover"]
    if current_conditions[0]["Pressure"]["Metric"]["Value"]:
        model_current_conditions.pressure = current_conditions[0]["Pressure"]["Metric"]["Value"]
    if current_conditions[0]["ApparentTemperature"]["Metric"]["Value"]:
        model_current_conditions.humidity_adjusted_temperature = current_conditions[
            0]["ApparentTemperature"]["Metric"]["Value"]
    if current_conditions[0]["WindChillTemperature"]["Metric"]["Value"]:
        model_current_conditions.wind_adjusted_temperature = current_conditions[
            0]["WindChillTemperature"]["Metric"]["Value"]
    if current_conditions[0]["Precip1hr"]["Metric"]["Value"]:
        model_current_conditions.rain_last_1hr = current_conditions[
            0]["Precip1hr"]["Metric"]["Value"]
    if current_conditions[0]["PrecipitationSummary"]["Past3Hours"]["Metric"]["Value"]:
        model_current_conditions.rain_last_3hr = current_conditions[
            0]["PrecipitationSummary"]["Past3Hours"]["Metric"]["Value"]
    if current_conditions[0]["EpochTime"]:
        model_current_conditions.timestamp = datetime.fromtimestamp(
            current_conditions[0]["EpochTime"])
    model_current_conditions.data_source = "accuweather"
    weathermodel.insert_api_current_condition(model_current_conditions)


if __name__ == "__main__":
    get_openweathermap()
    get_accuweather()
