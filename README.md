# Data Engineering Project : Parisian Mobility

![](/images/parisian_mobility_stack.png)


This project is developed as part of the Data Engineering bootcamp at Artefact School of Data.
It involves retrieving and processing data from multiple sources related to Paris transportation and weather. 
We implemented a data engineering flow using modern data stack principles:
- **Google Cloud Platform (GCP)** for infrastructure
- **BigQuery** for data storage and retrieval
- **Apache Airflow** for scheduling and orchestration of ETL (Extract, Transform, Load) processes.
- **DBT** (Data building Tool) core for data transformation using SQL

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

- **Metro Lines Perturbations**: Data on metro line disruptions from the Plateforme Régionale d'Information pour la Mobilité (PRIM).
- **Vélib' Stations**: Real-time data of Vélib' (Paris public bike rental service) stations.
- **Weather Conditions**: Weather data from Météo France.

## Data Sources

1. **[PRIM API](https://prim.iledefrance-mobilites.fr/fr/apis/idfm-disruptions_bulk)**: Provides information on public transportation disruptions.
2. **[Vélib' Open Data API](https://www.velib-metropole.fr/donnees-open-data-gbfs-du-service-velib-metropole)**: Offers real-time availability of bikes and stations.
3. **[Météo France API](https://open-meteo.com/en/docs/meteofrance-api#current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m&hourly=&timeformat=unixtime&forecast_days=1)**: Supplies weather forecasts and conditions.

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

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.in
```

### 3. Create a Google Cloud Project

Go to the Google Cloud Console.
Create a new project or use an existing one.
Note down the Project ID.

### 4. Configure Environment Variables

At the root of the project, create a .env file (this file is not versioned):

```bash
echo "PROJECT_ID=your-gcp-project-id" > .env
```
Replace your-gcp-project-id with your actual GCP project ID.

### 5. Update Pulumi Infrastructure Configuration
Copy the `infra/Pulumi.yaml.example` into `infra/Pulumi.yaml`
Open Pulumi.yaml and update the following fields:

```yaml
config:
  gcp:project: your-gcp-project-id
  gcp:region: your-region
  gcp:zone: your-zone
```
Replace your-gcp-project-id, your-region, and your-zone with your GCP project details.

```bash
make pulumi-install
```


### 6. Deploy Infrastructure to GCP

Use the Makefile to deploy the infrastructure:

```bash
make infra-up
```
This command uses Pulumi to create all necessary resources on GCP.

### 7. Set Up the Compute Engine VM

SSH into the VM:

```bash
gcloud compute ssh your-vm-instance-name --project=your-gcp-project-id
```
Replace your-vm-instance-name with the name of your VM instance.

Run the Installation Script:

```bash
sudo /opt/install.sh
```
This script installs all software dependencies required on the VM.

Clone the Project Repository on the VM:

```bash
gh repo clone pierrealexandre78/de_project
git clone https://github.com/pierrealexandre78/de_project.git
cd your_repository
```

Copy Configuration Files:

```bash
cp /opt/gcp_config.json src/config/
cp airflow/.env_example airflow/.env
```

Install the ETL Module:

```bash
pip install -e .  
```

## Running the Project

Start Airflow:

```bash
make run_airflow
```
This command starts the Airflow web server and scheduler.

## Accessing Airflow

Airflow Web Interface:

Open your web browser and navigate to http://your-vm-external-ip:8080.
Log in using the default credentials (if set) or your configured username and password.

## Airflow Configuration

Set Up Airflow Variables and Connections:

PRIM API Token: You'll need to create an account on PRIM to obtain an API token.

Log in to the Airflow web interface.

Navigate to Admin > Variables.

Add a new variable:

Key: PRIM_API_KEY
Value: Your PRIM API TOKEN

## Important Notes

PRIM API Account: Don't forget to create an account on PRIM and obtain your API token. This is essential for accessing the metro lines perturbation data.
API Keys and Tokens: Keep your API keys and tokens secure. Do not commit them to version control.
Environment Files: The .env files should not be versioned (.gitignore them) to prevent sensitive data from being exposed.
