import streamlit as st

st.set_page_config(
    page_title="DEmo Project Mobility",
    page_icon=":bar_chart:",
    layout="wide",
)

st.title("DE Project mobility Dashboard")
st.write("Welcome to the DE Project Dashboard!")
st.write("This dashboard provides insights into the DE Project mobility.")
st.write("Please select a page from the sidebar to explore further.")
st.markdown("""# Data Engineering Final Project
This project is developed as part of the Data Engineering bootcamp at Artefact School of Data. It involves retrieving and processing data from multiple sources related to Paris transportation and weather, leveraging Google Cloud Platform (GCP) for infrastructure, BigQuery for data storage, and Apache Airflow for orchestration of ETL (Extract, Transform, Load) processes.

## Table of Contents

- [Project Overview](#project-overview)
- [Data Sources](#data-sources)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Python Dependencies](#2-install-python-dependencies)
  - [3. Create a Google Cloud Project](#3-create-a-google-cloud-project)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Update Pulumi Infrastructure Configuration](#5-update-pulumi-infrastructure-configuration)
  - [6. Deploy Infrastructure to GCP](#6-deploy-infrastructure-to-gcp)
  - [7. Set Up the Compute Engine VM](#7-set-up-the-compute-engine-vm)
- [Airflow Configuration](#airflow-configuration)
- [Running the Project](#running-the-project)
- [Accessing Airflow](#accessing-airflow)

## Project Overview

The goal of this project is to build a data pipeline that collects, processes, and stores data from the following sources:

- **Paris Metro Lines Perturbations: Data on metro line disruptions from the Plateforme Régionale d'Information pour la Mobilité (PRIM).
- **Vélib' Stations: Real-time data of Vélib' (Paris public bike rental service) stations.
- **Weather Conditions in Paris: Weather data from Météo France.
## Data Sources

1. **PRIM API**: Provides information on public transportation disruptions.
2. **Vélib' Open Data API**: Offers real-time availability of bikes and stations.
3. **Météo France API**: Supplies weather forecasts and conditions.

## Architecture

The project uses the following technologies and services:

- **Google Cloud Platform (GCP)**: Hosts the infrastructure.
- **Google Compute Engine**: Runs the virtual machine for Airflow.
- **Google BigQuery**: Stores the processed data.
- **Apache Airflow**: Manages and orchestrates the ETL workflows.
- **Pulumi**: Infrastructure as code tool used for provisioning resources on GCP.
- **Python**: The primary programming language for the ETL processes.

## Prerequisites

- **Python 3.10 or higher**
- **Google Cloud SDK** installed and configured
- **Pulumi CLI** installed
- **Git** installed on your local machine
- **Make** utility installed
- **Account on [PRIM](https://prim.iledefrance-mobilites.fr/)** to obtain an API token
""")

