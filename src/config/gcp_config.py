import json
import os

# Open the gcp_config.json file at the same level as this file
config_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(config_dir, "gcp_config.json")

# Read and parse the JSON file
with open(file=config_path, mode="r", encoding="UTF-8") as config_file:
    config = json.load(config_file)


# Return a dictionary with the GCP configuration
def get_config() -> dict:
    return config
