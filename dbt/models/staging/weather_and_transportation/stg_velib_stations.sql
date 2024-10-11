select
    station_id,
    name,
    latitude,
    longitude,
    capacity
from {{ source("weather_and_transportation", "velib_stations") }}