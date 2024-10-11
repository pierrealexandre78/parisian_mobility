select
    name,
    latitude,
    longitude,
    line_id
from
    {{source("weather_and_transportation", "metro_stations")}} as stations
CROSS JOIN UNNEST(stations.line_id) AS line_id