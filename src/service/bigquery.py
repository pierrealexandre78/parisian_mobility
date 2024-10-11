from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
from config import gcp_config

# Initialize the BigQuery client
client = bigquery.Client()

# Get the GCP configuration
cloud_config = gcp_config.get_config()
project = cloud_config["project"]
dataset = cloud_config["dataset"]


def insert_rows(table_name, rows):

    # Set your table ID (replace with your actual project, dataset, and table)
    table_id = f"{project}.{dataset}.{table_name}"

    try:
        # print(f"Inserting {len(rows)} rows into {table_id}")

        # Get the table from the API
        table = client.get_table(table_id)
        
        # Attempt to insert rows
        client.insert_rows(table, rows)
    except GoogleAPIError as e:
        # Handle API errors
        print(f"An API error occurred: {e}")
    except Exception as e:
        # Handle unexpected exceptions
        print(f"An unexpected error occurred: {e}")
