select
    disruption_id,
    `begin` AS begin_time,
    `end` AS end_time,
    status,
    cause,
    category,
    effect,
    impacted_lines as line_id,
    impacted_stations,
    messages
from {{ source("weather_and_transportation", "metro_lines_status")}}