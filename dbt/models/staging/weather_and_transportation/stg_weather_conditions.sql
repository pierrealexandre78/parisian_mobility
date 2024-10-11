select
    time,
    apparent_temperature,
    precipitation,
    rain,
    showers
from {{ source('weather_and_transportation', 'weather_conditions')}}