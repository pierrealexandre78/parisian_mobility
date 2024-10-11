from typing import List
import requests, hashlib
from custom_types.velib_types import VelibStation, VelibStationStatus
from service import bigquery
from config import gcp_config

cloud_config = gcp_config.get_config()


def get_velib_stations():
    """
    format list containing velib stations Info from json file as dict
    only called once

    Args:
        raw_file (str): JSON file to format
    Returns:
        array: formated array containing velib stations Info, ready to be inserted in Big Query
    """

    # 1  get the data from the API

    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json"
    raw_data = requests.get(url, timeout=20).json()

    # 2 format the data
    raw_stations = raw_data["data"]["stations"]

    records: List[VelibStation] = []

    for station in raw_stations:
        formatted_result: VelibStation = {
            "station_id": station["station_id"],
            "name": station["name"],
            "latitude": station["lat"],
            "longitude": station["lon"],
            "capacity": station["capacity"],
        }
        # add the station to the global stations list
        records.append(formatted_result)

    # 3 insert the records in bigquery
    table_name = cloud_config["velib_stations_table"]
    bigquery.insert_rows(table_name, records)


def create_uid(id1, id2):
    # Combine the two IDs into a single string
    combined = f"{id1}-{id2}"

    # Generate a UUID based on the combined string
    unique_id = hashlib.md5(combined.encode()).hexdigest()
    return unique_id


def get_velib_stations_status():
    """
    format array containing velib stations status from json file as dict

    Args:
        raw_file (str): JSON file to format
    Returns:
        array: formated array containing velib stations status, ready to be inserted in Big Query
    """

    # 1 fetch station status from API

    # API url for station status
    url = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json"

    # request the api
    raw_data = requests.get(url, timeout=20).json()

    # 2 format the api response (raw_data) into records ready to be inserted in big query

    records: List[VelibStationStatus] = []

    # list of all the stations
    raw_stations = raw_data["data"]["stations"]

    for station in raw_stations:

        # skip stations that are not renting bikes : it means the station is empty of bikes
        if not station["is_renting"]:
            continue
        # converting last reported in posix to readable time for humans
        last_reported = station["last_reported"]

        # create unique id with station id and last reported date so it can be unique in bigquery
        uuid = create_uid(station["station_id"], last_reported)
        station_id = station["station_id"]
        num_bikes_available = station["num_bikes_available"]
        num_bikes_mechanical = station["num_bikes_available_types"][0]["mechanical"]
        num_bikes_ebikes = station["num_bikes_available_types"][1]["ebike"]
        num_docks_available = station["num_docks_available"]

        formatted_result: VelibStationStatus = {
            "uuid": uuid,
            "station_id": station_id,
            "num_bikes_available": num_bikes_available,
            "num_bikes_mechanical": num_bikes_mechanical,
            "num_bikes_ebike": num_bikes_ebikes,
            "num_docks_available": num_docks_available,
            "last_reported": last_reported,
        }
        # add the station to the global stations list
        records.append(formatted_result)

    # 3 insert the records in bigquery
    table_name = cloud_config["velib_stations_status_table"]
    bigquery.insert_rows(table_name, records)

# Main entry point
if __name__ == "__main__":
    get_velib_stations()
