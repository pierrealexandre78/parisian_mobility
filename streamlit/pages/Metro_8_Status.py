import streamlit as st
import pandas as pd
import pydeck as pdk
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime

# Initialize the BigQuery client
key_path = "dbt/service_account_key.json"
credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# Define a function to query the stations locations
def query_line8_stations_locations():
    query = """
    SELECT name, latitude, longitude
    FROM `de-project-pulumi.visualization.line_8_stations_locations`
    """
    try:
        return client.query(query).to_dataframe()
    except Exception as e:
        st.error(f"Erreur lors du chargement des stations du métro 8 : {e}")
        return pd.DataFrame()

# Define a function to query the disruptions
# def load_disruptions():
#     query = """
#     SELECT 
#         begin_time,
#         end_time,
#         status,
#         effect,
#         line_id,

#     FROM `de-project-pulumi.visualization.stg_metro_lines_status`
#     LIMIT 100
#     """
#     try:
#         return client.query(query).to_dataframe()
#     except Exception as e:
#         st.error(f"Erreur lors du chargement des perturbations : {e}")
#         return pd.DataFrame()

st.title("Metro Line 8: Geographical view")

df_line_stations = query_line8_stations_locations()

status_colors = {
    "NO_SERVICE": [255, 0, 0],
    "SIGNIFICANT_DELAYS": [255, 165, 0],
    "": [0, 255, 0]
}

# Create a scatter plot layer
scatter_plot = pdk.Layer(
    "ScatterplotLayer",
    data=df_line_stations,
    get_position=["longitude", "latitude"],
    get_radius=100,
    get_color=[255, 140, 0],
    get_width=20,
)

# Configurer la vue de la carte
view_state = pdk.ViewState(
    latitude=df_line_stations["latitude"].mean(),
    longitude=df_line_stations["longitude"].mean(),
    zoom=11,
    pitch=0
)

# Créer une carte avec PyDeck
r = pdk.Deck(
    layers=[scatter_plot],
    initial_view_state=view_state,
    tooltip={"text": "{name}"}
)

# Afficher la carte dans Streamlit
st.pydeck_chart(r)

# afficher le dataframe
st.dataframe(df_line_stations)

