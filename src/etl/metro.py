from typing import List
import re, json, requests
from config import gcp_config
from service import bigquery, storage
from custom_types.metro_types import (
    MetroStation,
    MetroLineRef,
    MetroLine,
    MetroLineStatus,
)

cloud_config = gcp_config.get_config()
project_id = cloud_config["project"]
bucket_name = cloud_config["metro-data_bucket"]
metro_lines_blob = cloud_config["metro-lines_blob"]
metro_stations_blob = cloud_config["metro-stations_blob"]

# Define the function to get metro lines and stations
def get_metro_lines_and_stations():

    stations_json = storage.download_as_json(bucket_name, metro_stations_blob)
    metro_stations: List[MetroStation] = []
    for station in stations_json:
        fields = station.get("fields")
        if "METRO" not in fields.get("mode"):
            continue

        line_ids = [line_id.strip() for line_id in fields.get("idrefligc").split('/')]
        coordinates = station.get("geometry").get("coordinates")
        formated_result: MetroStation = {
            "name": fields.get("nom_zdc"),
            "latitude": coordinates[1],
            "longitude": coordinates[0],
            "codeunique": fields.get("codeunique"),
            "line_id": line_ids,
        }
        metro_stations.append(formated_result)

    table_name = cloud_config["metro_stations_table"]
    bigquery.insert_rows(table_name, metro_stations)

    lines_json = storage.download_as_json(bucket_name, metro_lines_blob)
    metro_line_references: List[MetroLineRef] = []
    for line_entry in lines_json:
        formatted_result: MetroLineRef = {
            "id_line": line_entry.get("id_line"),
            "name_line": line_entry.get("name_line"),
        }
        metro_line_references.append(formatted_result)

    metro_lines: List[MetroLine] = []
    for line in metro_line_references:
        line_id = line.get("id_line")
        line_name = line.get("name_line")

        # Retrieve stations for the line
        line_stations = [ station.get("name") for station in metro_stations if line_id in station.get("line_id") ]
        formatted_result: MetroLine = {
            "id": line_id,
            "line_name": line_name,
            "stations_names": line_stations,
        }
        metro_lines.append(formatted_result)

    # Insert data to BigQuery tables for stations and lines
    table_name = cloud_config["metro_lines_table"]
    bigquery.insert_rows(table_name, metro_lines)


def get_metro_lines_status(**context):
    prim_api_key = context.get("PRIM_API_KEY")
    prim_api_url = "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/line_reports/physical_modes/physical_mode:Metro/line_reports"

    params = {"count": 100, "since": "20240920T000000"}

    response = requests.get(
        prim_api_url, params=params, timeout=20, headers={"apiKey": prim_api_key}
    )

    raw_data = response.json()["disruptions"]

    status_records: List[MetroLineStatus] = []

    for disruption in raw_data:
        impacted_objects = ", ".join(
            [obj["pt_object"]["name"] for obj in disruption["impacted_objects"]]
        )
        status = disruption["status"]

        # continue if the status is not active or if the impacted objects do not contain 'Métro'
        if "Métro" in impacted_objects and status == "active":
            # Clean up messages of html formatings
            messages = [message["text"] for message in disruption["messages"]]
            messages = [re.sub(r"<[^>]+>", "", message) for message in messages]
            messages = [
                message.replace("Plus d'informations sur le site ratp.fr", "")
                for message in messages
            ]

            # Retrieve impacted station names
            impacted_stations: List[str] = []

            # Retrieve impacted line ids
            impacted_objects = ", ".join(
                [obj["pt_object"]["id"] for obj in disruption["impacted_objects"]]
            )
            idrefligc_pattern = r"C\d+"
            impacted_idrefligcs: List[str] = re.findall(
                idrefligc_pattern, impacted_objects
            )

            formatted_result: MetroLineStatus = {
                "disruption_id": disruption["disruption_id"],
                "begin": disruption["application_periods"][-1]["begin"],
                "end": disruption["application_periods"][-1]["end"],
                "status": status,
                "cause": disruption["cause"],
                "category": disruption["category"],
                "effect": disruption["severity"]["effect"],
                "messages": messages,
                "impacted_stations": impacted_stations,
                "impacted_lines": impacted_idrefligcs,
            }
            status_records.append(formatted_result)

    # Return if there are no records to insert
    if not status_records:
        return

    status_records = json.dumps(status_records, ensure_ascii=False)

    records = json.loads(status_records)
    table_name = cloud_config["metro_lines_status_table"]
    bigquery.insert_rows(table_name, records)

# Main entry point
if __name__ == "__main__":
    get_metro_lines_and_stations()
