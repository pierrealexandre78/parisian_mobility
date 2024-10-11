select
    name,
    latitude,
    longitude
    
from {{ ref('stg_metro_stations')}}
where line_id = 'C01378'
