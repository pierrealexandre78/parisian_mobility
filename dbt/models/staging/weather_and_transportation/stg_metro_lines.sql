select
    id as line_id,
    line_name,
    station_name
from {{ source("weather_and_transportation", "metro_lines")}} as lines
CROSS JOIN UNNEST(lines.stations_names) AS station_name