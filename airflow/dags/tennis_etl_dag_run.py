from datetime import timedelta, datetime
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

from transform.job import transform_tennis_data
from load.job import clean_and_load_tennis_data, upload_tennis_data_to_gcs

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BASE_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
DOWNLOAD_DIRECTORY = "downloads"
FULL_DOWNLOAD_PATH = f'{AIRFLOW_HOME}/dags/{DOWNLOAD_DIRECTORY}'

MATCH_YEARS=(2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022)

RANK_YEARS=('00s', '10s', '20s')

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DESTINATION_BUCKET = os.environ.get("GCP_GCS_BUCKET")

TENNIS_DATASET = 'atp_tennis_data'
PLAYERS_TABLE = 'atp_players'
MATCHES_TABLE = 'atp_matches'
RANKINGS_TABLE = 'atp_rankings'

DBT_JOB_ID = os.environ.get("DBT_JOB_ID")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 1, 1), #airflow.utils.dates.days_ago(2),
    'retry_delay': timedelta(minutes=1),
    'retry': 2,
    'email_on_failure': False,
    'email_on_retry': False,
    "email": [os.getenv("ALERT_EMAIL", "")],
}

with DAG(
    'tennis_etl_dag_run',
    default_args = default_args,
    description = 'ETL for tennis data',
    schedule_interval="@once", #for one time
    catchup=True,
    tags=['tennis_etl', 'tennis_etl_dag_run'],
    max_active_runs=5,
) as dag:

    start = EmptyOperator(task_id="start")

    t1 = BashOperator(
        task_id='extract_files',
        bash_command=f'{AIRFLOW_HOME}/dags/extract/job.sh {BASE_URL} {FULL_DOWNLOAD_PATH} ',
    )

    # python operator to convert to parquet
    t2 = PythonOperator(
        task_id='transform_to_parquet',
        python_callable=transform_tennis_data,
        op_kwargs={'PG_USER': PG_USER, 'PG_PASSWORD': PG_PASSWORD, 'PG_HOST': PG_HOST, 'PG_PORT': PG_PORT, 'PG_DATABASE': PG_DATABASE, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS, 'FILE_SAVE_LOCATION': FULL_DOWNLOAD_PATH},
    )
    
    t3a = PostgresOperator(
        task_id="drop_tennis_db",
        postgres_conn_id="postgres_default",
        sql="DROP DATABASE IF EXISTS atp_tennis_2000_2022;",
        autocommit=True,
        dag=dag,
    )
    t3b = PostgresOperator(
        task_id="create_tennis_db",
        postgres_conn_id="postgres_default",
        sql="CREATE DATABASE atp_tennis_2000_2022;",
        autocommit=True,
        dag=dag,
    )

    # python operator to clean and load to postgres
    t4 = PythonOperator(
        task_id='clean_and_load',
        python_callable=clean_and_load_tennis_data,
        op_kwargs={'PG_USER': PG_USER, 'PG_PASSWORD': PG_PASSWORD, 'PG_HOST': PG_HOST, 'PG_PORT': PG_PORT, 'PG_DATABASE': PG_DATABASE, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS, 'FILE_PATH': FULL_DOWNLOAD_PATH},
        dag=dag
    )
    

    # python operator to upload to gcs
    t5 = PythonOperator(
        task_id='upload_to_gcs',
        python_callable=upload_tennis_data_to_gcs,
        op_kwargs={'destination_bucket': DESTINATION_BUCKET, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS, 'FILE_PATH': FULL_DOWNLOAD_PATH},
        dag=dag
    )

    t6 =  GCSToBigQueryOperator(
            task_id = f'create_table_players',
            bucket=f"{DESTINATION_BUCKET}",
            source_format='PARQUET',
            source_objects=[f"{TENNIS_DATASET}/{PLAYERS_TABLE}/*.parquet"],
            destination_project_dataset_table=f"{PROJECT_ID}.{TENNIS_DATASET}.{PLAYERS_TABLE}",
            autodetect=True,
            write_disposition="WRITE_TRUNCATE",
    )
    
    t7 =  GCSToBigQueryOperator(
            task_id = f'create_table_matches',
            bucket=f"{DESTINATION_BUCKET}",
            source_format='PARQUET',
            source_objects=[f"{TENNIS_DATASET}/{MATCHES_TABLE}/*.parquet"],
            destination_project_dataset_table=f"{PROJECT_ID}.{TENNIS_DATASET}.{MATCHES_TABLE}",
            autodetect=True,
            write_disposition="WRITE_APPEND",
    )
    
    t8 =  GCSToBigQueryOperator(
            task_id = f'create_table_rankings',
            bucket=f"{DESTINATION_BUCKET}",
            source_format='PARQUET',
            source_objects=[f"{TENNIS_DATASET}/{RANKINGS_TABLE}/*.parquet"],
            destination_project_dataset_table=f"{PROJECT_ID}.{TENNIS_DATASET}.{RANKINGS_TABLE}",
            autodetect=True,
            write_disposition="WRITE_APPEND",
    )
    
    # Docs: https://airflow.apache.org/docs/apache-airflow-providers-dbt-cloud/stable/index.html
    # a free dbt cloud account can't use the dbt cloud api so this will fail, alternative is to run dbt locally
    t9 = DbtCloudRunJobOperator(
        task_id="run_dbt_job",
        job_id=DBT_JOB_ID,
        check_interval=10,
        timeout=300,
    )

    t10 = BashOperator(
        task_id='delete_files',
        bash_command=f'rm -r {FULL_DOWNLOAD_PATH}',
        dag=dag
    )

    end = EmptyOperator(task_id="end")

start >> t1 >> t2 >> t3a >> t3b >> t4 >> t5
t5 >> [t6, t7, t8] >> t10 >> end