from typing import NamedTuple


class WeatherConditions(NamedTuple):
    latitude: float
    longitude: float
    elevation: int
    time: int
    temperature_2m: float
    relative_humidity_2m: float
    apparent_temperature: float
    is_day: int
    precipitation: float
    rain: int
    showers: int
    snowfall: int
    weather_code: int
    cloud_cover: int
    pressure_msl: float
    surface_pressure: float
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float
