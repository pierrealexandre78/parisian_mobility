select
    uuid,
    station_id,
    num_bikes_available,
    num_bikes_mechanical,
    num_bikes_ebike,
    num_docks_available,
    last_reported
from {{ source("weather_and_transportation", "velib_stations_status")}}