from typing import NamedTuple


class VelibStation(NamedTuple):
    station_id: int
    name: str
    latitude: float
    longitude: float
    capacity: int


class VelibStationStatus(NamedTuple):
    uuid: int
    station_id: int
    num_bikes_available: int
    num_bikes_mechanical: int
    num_bikes_ebike: int
    num_docks_available: int
    is_renting: int
    last_updated_other: int
    last_reported: int
