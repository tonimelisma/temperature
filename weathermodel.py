#!/usr/bin/python3
#
# Copyright (c) Toni Melisma 2022

import meteocalc
from sqlalchemy import Column, String, DateTime, Float, Integer, create_engine, select
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
#engine = create_engine("sqlite:///db.sqlite", echo=True, future=True)
engine = create_engine("sqlite:////home/toni/db.sqlite", future=True)


# Data model

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)

    def __repr__(self):
        return f"Measurement(id={self.id!r}, timestamp={self.timestamp!r}, temperature={self.temperature!r} C, pressure={self.pressure!r} hPa, humidity={self.humidity!r} % rH)"


class APICurrentCondition(Base):
    __tablename__ = "api_current_condition"
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime, index=True)
    data_source = Column(String)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    wind_gust_speed = Column(Float)
    weather_condition = Column(String)
    cloudiness = Column(Float)
    rain_last_1hr = Column(Float)
    rain_last_3hr = Column(Float)
    visibility = Column(Integer)
    uv_index = Column(Integer)
    feels_like_temperature = Column(Float)
    feels_like_shade_temperature = Column(Float)
    humidity_adjusted_temperature = Column(Float)
    wind_adjusted_temperature = Column(Float)

# Initialize datamodel


def initialize():
    Base.metadata.create_all(engine)


def insert_measurement(new_measurement):
    if not isinstance(new_measurement, Measurement):
        raise ValueError("parameter is not a valid measurement")
    if (not new_measurement.id or not new_measurement.timestamp
        or not new_measurement.temperature or not new_measurement.pressure
            or not new_measurement.humidity):
        raise ValueError("missing values for measurement")
    with Session(engine) as session:
        session.add(new_measurement)
        session.commit()


def insert_api_current_condition(new_api_reading):
    if not isinstance(new_api_reading, APICurrentCondition):
        raise ValueError("parameter is not a valid reading")
    if (not new_api_reading.timestamp or not new_api_reading.temperature or not new_api_reading.pressure or not new_api_reading.humidity or not new_api_reading.wind_speed):
        raise ValueError("missing required values for API reading")
    with Session(engine) as session:
        session.add(new_api_reading)
        session.commit()


def select_latest_measurement():
    session = Session(engine)
    stmt = select(Measurement).order_by(Measurement.timestamp.desc())
    this_measurement = session.scalars(stmt).first()
    return (this_measurement)


def select_last7days_measurements():
    session = Session(engine)
    stmt = select(Measurement).order_by(Measurement.timestamp.desc()).limit(10080)
    measurements = session.scalars(stmt)
    return (measurements)


def calculate_latest_average_windspeed():
    session = Session(engine)
    ds1_stmt = select(APICurrentCondition).where(APICurrentCondition.data_source ==
                                                 "accuweather").order_by(APICurrentCondition.timestamp.desc())
    ds1_data = session.scalars(ds1_stmt).first()
    ds2_stmt = select(APICurrentCondition).where(APICurrentCondition.data_source ==
                                                 "openweathermap").order_by(APICurrentCondition.timestamp.desc())
    ds2_data = session.scalars(ds2_stmt).first()
    average_windspeed = (ds1_data.wind_speed + ds2_data.wind_speed) / 2
    return (average_windspeed)


if __name__ == "__main__":
    # bob = Measurement(
    #    id="xyz3",
    #    timestamp=datetime.now(),
    #    temperature=20.1,
    #    pressure=1080.4,
    #    humidity=75.2
    # )
    # try:
    #    insert_measurement(bob)
    # except Exception:
    #    logging.error("Unspecified error: " + repr(Exception))
    # print(select_latest_measurement())
    initialize()
    # print(calculate_latest_average_windspeed())
