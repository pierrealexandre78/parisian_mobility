from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import EmptyOperator
from airflow.operators.python import PythonOperator

import sys, os
sys.path.append(os.path.abspath("/opt/airflow/src"))

from etl import metro, velib

with DAG(
    "static_data_dag",
    description="Velib and Metro static data DAG"
    # run the DAG only once
    ,
    schedule_interval="@once",
    start_date=datetime(2017, 9, 18),  # start date of the DAG
    catchup=False,  # set to False to skip any intervals you missed while the DAG was not running
) as dag:

    # Define the tasks, EmptyOperator is a dummy operator that does nothing ✅
    start = EmptyOperator(task_id="start", owner="lolo")
    end = EmptyOperator(task_id="end", owner="lolo")

    task_metro_lines_and_stations = PythonOperator(
        task_id="get_metro_lines_and_stations",
        python_callable=metro.get_metro_lines_and_stations,
        dag=dag,
    )

    task_velib_stations = PythonOperator(
        task_id="get_velib_stations",
        python_callable=velib.get_velib_stations,
        dag=dag,
    )

    # Define the order of the tasks
    start >> task_metro_lines_and_stations >> task_velib_stations >> end
