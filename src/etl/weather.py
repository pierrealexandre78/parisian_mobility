from typing import List
import requests
from service import bigquery
from custom_types.weather_types import WeatherConditions
from config import gcp_config

base_url = "https://api.open-meteo.com/v1/forecast?"

cloud_config = gcp_config.get_config()


def get_weather_conditions(latitude: float = 48.8533, longitude: float = 2.3485) -> str:
    """ """
    # 1 fetch current weather from api

    # Current weather parameters
    current_params = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "is_day",
        "precipitation",
        "rain",
        "showers",
        "snowfall",
        "weather_code",
        "cloud_cover",
        "pressure_msl",
        "surface_pressure",
        "wind_speed_10m",
        "wind_direction_10m",
        "wind_gusts_10m",
    ]
    current_params_str = ",".join(current_params)

    # URL parameters
    timeformat = "unixtime"
    forecast_days = 0
    model = "meteofrance_seamless"

    # Construct the URL
    url = f"{base_url}latitude={latitude}&longitude={longitude}&current={current_params_str}&timeformat={timeformat}&forecast_days={forecast_days}&models={model}"

    # Fetch the data
    raw_data = requests.get(url=url, timeout=20).json()

    # 2 format the api response (raw_data) into records ready to be inserted in big query

    records: List[WeatherConditions] = [
        {
            "latitude": raw_data.get("latitude"),
            "longitude": raw_data.get("longitude"),
            "elevation": raw_data.get("elevation"),
            "time": raw_data.get("current").get("time"),
            "temperature_2m": raw_data.get("current").get("temperature_2m"),
            "relative_humidity_2m": raw_data.get("current").get("relative_humidity_2m"),
            "apparent_temperature": raw_data.get("current").get("apparent_temperature"),
            "is_day": raw_data.get("current").get("is_day"),
            "precipitation": raw_data.get("current").get("precipitation"),
            "rain": raw_data.get("current").get("rain"),
            "showers": raw_data.get("current").get("showers"),
            "snowfall": raw_data.get("current").get("snowfall"),
            "weather_code": raw_data.get("current").get("weather_code"),
            "cloud_cover": raw_data.get("current").get("cloud_cover"),
            "pressure_msl": raw_data.get("current").get("pressure_msl"),
            "surface_pressure": raw_data.get("current").get("surface_pressure"),
            "wind_speed_10m": raw_data.get("current").get("wind_speed_10m"),
            "wind_direction_10m": raw_data.get("current").get("wind_direction_10m"),
            "wind_gusts_10m": raw_data.get("current").get("wind_gusts_10m"),
        }
    ]

    # 3 load the current records in bigquery
    table_name = cloud_config["weather_conditions_table"]
    bigquery.insert_rows(table_name, records)
