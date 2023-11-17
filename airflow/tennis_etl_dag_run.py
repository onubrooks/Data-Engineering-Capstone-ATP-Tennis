from datetime import timedelta
import os
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator, PythonOperator

from transform.job import transform_tennis_data
from load.job import clean_and_load_tennis_data

GH_BASE_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')
FILE_SAVE_LOCATION = "downloads"

MATCH_YEARS=(2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)

RANK_YEARS=('00s', '10s', '20s')

default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'retry_delay': timedelta(minutes=5),
    'retry': 1
}

dag = DAG('download_and_delete_files_dag', default_args=default_args, schedule_interval=timedelta(minutes=10))

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

t9 = BashOperator(
    task_id='delete_files',
    bash_command='rm -r downloads',
    dag=dag
)

t1 >> t3