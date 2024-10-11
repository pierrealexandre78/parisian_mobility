from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import EmptyOperator
from airflow.operators.python import PythonOperator

import sys, os
sys.path.append(os.path.abspath("/opt/airflow/src"))
from etl import weather

with DAG(
    "dynamic_weather_dag",
    description="Meteo France API DAG"
    # run the DAG every 60 minutes
    ,
    schedule_interval=timedelta(minutes=60),
    start_date=datetime(2017, 9, 18),  # start date of the DAG
    catchup=False,  # set to False to skip any intervals you missed while the DAG was not running
) as dag:

    # Define the tasks, EmptyOperator is a dummy operator that does nothing ✅
    start = EmptyOperator(task_id="start", owner="lolo")
    end = EmptyOperator(task_id="end", owner="lolo")

    task = PythonOperator(
        task_id="my_python_task",
        python_callable=weather.get_weather_conditions,
        dag=dag,
    )

    # Define the order of the tasks
    start >> task >> end
