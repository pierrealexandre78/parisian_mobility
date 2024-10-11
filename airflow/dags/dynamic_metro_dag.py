from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable

import sys, os
sys.path.append(os.path.abspath("/opt/airflow/src"))
from etl import metro

with DAG(
    "dynamic_metro_dag",
    description="PRIM API DAG"
    # run the DAG every 10 minutes
    ,
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2017, 9, 18),  # start date of the DAG
    catchup=False,  # set to False to skip any intervals you missed while the DAG was not running
) as dag:

    # Define the tasks, EmptyOperator is a dummy operator that does nothing ✅
    start = EmptyOperator(task_id="start", owner="lolo")
    end = EmptyOperator(task_id="end", owner="lolo")

    task = PythonOperator(
        task_id="my_python_task",
        python_callable=metro.get_metro_lines_status,
        dag=dag,
        # pass the API key as a context variable
        op_kwargs={"PRIM_API_KEY": Variable.get("PRIM_API_KEY")},
    )

    # Define the order of the tasks
    start >> task >> end
