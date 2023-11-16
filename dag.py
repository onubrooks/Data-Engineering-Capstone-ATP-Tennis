from datetime import timedelta
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

GH_BASE_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/"
FILE_SAVE_LOCATION = "downloads"

# db_engine = get_db_conn_engine(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
match_years=(2000, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019)
rank_years=('00s', '10s')

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

t1 = BashOperator(
    task_id='download_files',
    bash_command='sh download_files.sh {{ params.download_url }} {{ params.file_save_location }}',
    params={'base_url': GH_BASE_URL, 'file_save_location': FILE_SAVE_LOCATION},
    dag=dag
)

t3 = BashOperator(
    task_id='delete_files',
    bash_command='rm -r downloads',
    dag=dag
)

t1 >> t3