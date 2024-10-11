from typing import NamedTuple, List


class MetroLineRef(NamedTuple):
    id_line: str
    name_line: str


class MetroStation(NamedTuple):
    name: str
    latitude: float
    longitude: float
    codeunique: int
    line_id: List[str]


class MetroLine(NamedTuple):
    id: str
    line_name: str
    stations_names: List[str]


class MetroLineStatus(NamedTuple):
    disruption_id: str
    begin: str
    end: str
    status: str
    cause: str
    category: str
    effect: str
    impacted_lines: List[str]
    impacted_stations: List[str]
    messages: List[str]
