"""A Google Cloud Python Pulumi program to setup a GCP Storage Bucket and 
BigQuery Dataset with tables."""

import pulumi
import json
from pulumi_gcp import storage
from pulumi_gcp import bigquery
from pulumi_gcp import compute

lines_filename = "./data-bucket/referentiel-des-lignes.json"
stations_filename = "./data-bucket/emplacement-des-gares-idf-data-generalisee.json"

# Read the configuration values for GCP
gcp_config = pulumi.Config("gcp")
project = gcp_config.require("project")
location = gcp_config.require("region")
zone = gcp_config.require("zone")


# Create a GCP resource (Storage Bucket)
setup_bucket = storage.Bucket('setup-bucket', location=location)

# Create a Storage Bucket Object for the install shell script
install_bucket_file = storage.BucketObject(
    'install.sh', bucket=setup_bucket.name, source=pulumi.FileAsset('./airflow-vm/install.sh')
)

# Create a GCP resource (Storage Bucket)
bucket = storage.Bucket('static-data-bucket', location=location)

# Create a Storage Bucket Object for the lines and stations data
bucket_object_lines = storage.BucketObject(
    'metro-lines', bucket=bucket.name, source=pulumi.FileAsset(lines_filename)
)

bucket_object_stations = storage.BucketObject(
    'metro-stations', bucket=bucket.name, source=pulumi.FileAsset(stations_filename)
)

# Create a BigQuery Dataset for the visualization
visualization_dataset = bigquery.Dataset(
    "visualization-dataset",
    dataset_id="visualization",
    friendly_name="Visualization for the Weather and Transportation Data",
    description="Visualization for the weather and transportation data for the Paris region",
    location=location,
    labels={"env": "dev"}
)

# Create a BigQuery Dataset for the weather and transportation data
weather_transportation_dataset = bigquery.Dataset(
    "weather-and-transportation-dataset",
    dataset_id="weather_and_transportation",
    friendly_name="Weather and Transportation Data",
    description="Weather and transportation data for the Paris region",
    location=location,
    labels={"env": "dev"}
)

# Create the metro stations table
metro_stations_table = bigquery.Table(
    "metroStationsTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="metro_stations",
    schema="""[
        {"name": "name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "codeunique", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "line_id", "type": "STRING", "mode": "REPEATED"}
    ]""",
    deletion_protection=False
)

# Create the metro lines table
metro_lines_table = bigquery.Table(
    "metroLinesTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="metro_lines",
    schema="""[
        {"name": "id", "type": "STRING"},
        {"name": "line_name", "type": "STRING"},
        {"name": "stations_names", "type": "STRING", "mode": "REPEATED"}
    ]""",
    deletion_protection=False
)

# Create the metro lines status table
metro_lines_status_table = bigquery.Table(
    "metroLinesStatusTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="metro_lines_status",
    schema="""[
                {"name": "disruption_id", "type": "STRING" },
                {"name": "begin", "type": "STRING"},
                {"name": "end", "type": "STRING"},
                {"name": "status", "type": "STRING"},
                {"name": "cause", "type": "STRING"},
                {"name": "category", "type": "STRING"},
                {"name": "effect", "type": "STRING"},
                {"name": "impacted_lines", "type": "STRING", "mode": "REPEATED"},
                {"name": "impacted_stations", "type": "STRING", "mode": "REPEATED"},
                {"name": "messages", "type": "STRING", "mode": "REPEATED"}
    ]""",
    deletion_protection=False
)

# Create the velib stations table
velib_stations_table = bigquery.Table(
    "velibStationsTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="velib_stations",
    schema="""[
            {"name": "station_id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "capacity", "type": "INTEGER", "mode": "NULLABLE"}
    ]""",
    deletion_protection=False
)

# Create the velib stations status table
velib_stations_status_table = bigquery.Table(
    "velibStationsStatusTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="velib_stations_status",
    schema="""[
            {"name": "uuid", "type": "STRING", "mode": "NULLABLE"},
            {"name": "station_id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "num_bikes_available", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "num_bikes_mechanical", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "num_bikes_ebike", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "num_docks_available", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "last_reported", "type": "INTEGER", "mode": "NULLABLE"}
    ]""",
    deletion_protection=False
)

# Create the weather conditions table
weather_conditions_table = bigquery.Table(
    "WeatherConditionsTable",
    dataset_id=weather_transportation_dataset.dataset_id,
    table_id="weather_conditions",
    schema="""[
            {"name": "time", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "latitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "longitude", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "elevation", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "temperature_2m", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "relative_humidity_2m", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "apparent_temperature", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "is_day", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "precipitation", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "rain", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "showers", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "snowfall", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "weather_code", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "cloud_cover", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "pressure_msl", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "surface_pressure", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "wind_speed_10m", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "wind_direction_10m", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "wind_gusts_10m", "type": "FLOAT", "mode": "NULLABLE"}
    ]""",
    deletion_protection=False
)

# Collect the names of the created bucket objects
file_names_output = pulumi.Output.all(project,
                                      location,
                                      bucket.name, 
                                      bucket_object_lines.name, 
                                      bucket_object_stations.name,
                                      weather_transportation_dataset.dataset_id,
                                      metro_stations_table.table_id,
                                      metro_lines_table.table_id,
                                      metro_lines_status_table.table_id,
                                      velib_stations_table.table_id,
                                      velib_stations_status_table.table_id,
                                      weather_conditions_table.table_id).apply(
    lambda names: {'project': names[0], 
                   'location': names[1], 
                   'metro-data_bucket': names[2], 
                   'metro-lines_blob': names[3], 
                   'metro-stations_blob': names[4],
                   'dataset': names[5],
                   'metro_stations_table': names[6],
                   'metro_lines_table': names[7],
                   'metro_lines_status_table': names[8],
                   'velib_stations_table': names[9],
                   'velib_stations_status_table': names[10],
                   'weather_conditions_table': names[11]}
)

# Write the collected names to a JSON file locally
file_names = file_names_output.apply(lambda names: json.dumps(names, indent=2))

def write_to_local_file(content):
    with open('gcp_config.json', 'w') as f:
        f.write(content)

file_names.apply(write_to_local_file)

# Export a message stating the file was created locally
pulumi.export("local_json_file", "gcp_config.json created locally")

# Write the collected names to a JSON file in a bucket for the VM to access
gcp_config_json = file_names_output.apply(lambda names: pulumi.StringAsset(json.dumps(names, indent=2)))
gcp_config_bucket_object = storage.BucketObject(
    'gcp_config',
    bucket=setup_bucket.name,
    source=gcp_config_json,
    name="gcp_config.json"
)

# Export the URL of the JSON file
pulumi.export("gcp_config_url", gcp_config_bucket_object.id.apply(
    lambda id: f"https://storage.googleapis.com/{bucket.name}/{id}"
))

# Read the configuration values for the VM
vm_config = pulumi.Config("vm")
machine_type = vm_config.require("machineType")
os_image = vm_config.require("osImage")
disk_size = vm_config.require("diskSizeGb")
disk_type = vm_config.require("diskType")

# Define the startup script for the VM to install Docker, Docker Compose, and run the docker-compose file
startup_script = f"""
#!/bin/bash

sudo ufw allow 8080
sudo ufw allow 22

export BUCKET_URL=$(sudo bash -c "gcloud storage ls | grep setup")
export INSTALL_FILE_PATH=$(sudo bash -c "gcloud storage ls $BUCKET_URL | grep install")
export GCP_CONFIG_FILE_PATH=$(sudo bash -c "gcloud storage ls $BUCKET_URL | grep gcp_config")

sudo gsutil cp $INSTALL_FILE_PATH /opt/install.sh
sudo gsutil cp $GCP_CONFIG_FILE_PATH /opt/gcp_config.json
sudo chmod +x /opt/install.sh

"""

# Create a new network for the virtual machine.
network = compute.Network(
    "network",
    auto_create_subnetworks=False,
)

# Create a subnet on the network.
subnet = compute.Subnetwork(
    "subnet",
    ip_cidr_range="10.0.1.0/24",
    network=network.id,
    region=location,
)

# Create a firewall allowing inbound access over ports 80 (for HTTP) and 22 (for SSH).
firewall = compute.Firewall(
    "firewall",
    network=network.self_link,
    allows=[
        {
            "protocol": "tcp",
            "ports": [
                "22",
                "8080",
            ],
        },
    ],
    direction="INGRESS",
    source_ranges=[
        "0.0.0.0/0",
    ],
    target_tags=[
        "webserver",
    ],
)

# Create the virtual machine.
instance = compute.Instance(
    "instance",
    machine_type=machine_type,
    zone=zone,
    boot_disk=compute.InstanceBootDiskArgs(
        initialize_params=compute.InstanceBootDiskInitializeParamsArgs(
            size=disk_size,
            type=disk_type,
            image=os_image 
        )),
    network_interfaces=[
        {
            "network": network.id,
            "subnetwork": subnet.id,
            "access_configs": [
                {},
            ],
        },
    ],
    service_account={
        "scopes": [
            "https://www.googleapis.com/auth/cloud-platform",
        ],
    },
    allow_stopping_for_update=True,
    metadata_startup_script=startup_script,
    tags=[
        "webserver",
    ],
    opts=pulumi.ResourceOptions(depends_on=firewall),
)

instance_ip = instance.network_interfaces.apply(
    lambda interfaces: interfaces[0].access_configs
    and interfaces[0].access_configs[0].nat_ip
)

# Export the instance's name, public IP address, and HTTP URL.
pulumi.export("name", instance.name)
pulumi.export("ip", instance_ip)
pulumi.export("url", instance_ip.apply(lambda ip: f"http://{ip}:{8080}"))
