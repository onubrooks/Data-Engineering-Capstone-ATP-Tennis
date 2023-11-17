from datetime import timedelta, datetime
import os
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator, PythonOperator, EmptyOperator

from transform.job import transform_tennis_data
from load.job import clean_and_load_tennis_data, upload_tennis_data_to_gcs

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
GH_BASE_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
FILE_SAVE_LOCATION = "downloads"

MATCH_YEARS=(2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)

RANK_YEARS=('00s', '10s', '20s')

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DESTINATION_BUCKET = os.environ.get("GCP_GCS_BUCKET")

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'retry_delay': timedelta(minutes=1), #datetime(2020, 1, 1)
    'retry': 2,
    'email_on_failure': False,
    'email_on_retry': False,
    "email": [os.getenv("ALERT_EMAIL", "")],
}

dag = DAG(
    dag_id = f'tennis_etl_dag_run',
    default_args = default_args,
    description = f'Execute only once to create songs table in bigquery',
    schedule_interval="@once", #At the 5th minute of every hour 
    # "0 6 2 * *" #At 6:00 am on the 2nd day of every month
    start_date=datetime(2022,3,20),
    end_date=datetime(2022,3,20),
    catchup=True,
    tags=['tennis_etl', 'tennis_etl_dag_run'],
    max_active_runs=1,
)

start = EmptyOperator(task_id="start")

t1 = BashOperator(
    task_id='make_script_executable',
    bash_command='chmod +x download_files.sh',
    dag=dag
)

t2 = BashOperator(
    task_id='extract_files',
    bash_command='sh extract/download_files.sh {{ params.download_url }} {{ params.file_save_location }}',
    params={'download_url': GH_BASE_URL, 'file_save_location': FILE_SAVE_LOCATION},
    dag=dag
)

# python operator to convert to parquet
t3 = PythonOperator(
    task_id='transform_to_parquet',
    python_callable=transform_tennis_data,
    op_kwargs={'PG_USER': PG_USER, 'PG_PASSWORD': PG_PASSWORD, 'PG_HOST': PG_HOST, 'PG_PORT': PG_PORT, 'PG_DATABASE': PG_DATABASE, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS},
    dag=dag
)

# python operator to clean and load to postgres
t4 = PythonOperator(
    task_id='clean_and_load',
    python_callable=clean_and_load_tennis_data,
    op_kwargs={'PG_USER': PG_USER, 'PG_PASSWORD': PG_PASSWORD, 'PG_HOST': PG_HOST, 'PG_PORT': PG_PORT, 'PG_DATABASE': PG_DATABASE, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS},
    dag=dag
)

# python operator to upload to gcs
t5 = PythonOperator(
    task_id='upload_to_gcs',
    python_callable=upload_tennis_data_to_gcs,
    op_kwargs={'destination_bucket': DESTINATION_BUCKET, 'MATCH_YEARS': MATCH_YEARS, 'RANK_YEARS': RANK_YEARS},
    dag=dag
)

t9 = BashOperator(
    task_id='delete_files',
    bash_command='rm -r downloads',
    dag=dag
)

end = EmptyOperator(task_id="end")

start >> t1 >> t2 >> t3 >> t4 >> t5 >> t9 >> end