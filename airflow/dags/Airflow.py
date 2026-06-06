from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


import sys
sys.path.insert(0, '/opt/airflow/project')
from Data_Ingestion.Data_Ingestion import main as data_ingestion_main
from duck_db_setup.staging import main as staging_main


with DAG(
        'simple_dag',
        start_date=datetime(2023, 1, 1),
        schedule_interval='@daily',
        catchup=False
) as dag:
    task1 = PythonOperator(
        task_id='Data_Ingestion',
        python_callable=data_ingestion_main
    )
    task2 = PythonOperator(
        task_id='Staging',
        python_callable=staging_main
    )
    task3 = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/project/weather_pipeline && dbt run'
    )

    task4 = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/project/weather_pipeline && dbt test'
    )

    task1 >> task2 >> task3 >> task4
