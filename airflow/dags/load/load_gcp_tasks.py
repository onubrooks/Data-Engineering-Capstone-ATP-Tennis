"""
Airflow Docs: https://airflow.apache.org/docs/apache-airflow-providers-google/stable/operators/cloud/index.html
"""

from airflow.providers.google.cloud.hooks.gcs import GCSHook

TENNIS_DIRECTORY = 'atp_tennis_data'
PLAYERS_TABLE = f'{TENNIS_DIRECTORY}/atp_players'
MATCHES_TABLE = f'{TENNIS_DIRECTORY}/atp_matches'
RANKINGS_TABLE = f'{TENNIS_DIRECTORY}/atp_rankings'

gcs_hook = GCSHook(
    gcp_conn_id="google_cloud_default",
    delegate_to=None,
    impersonation_chain=None,
)
def run_gcs_task(destination_bucket, prefix, pq_file, local_file):
    """run gcs task to upload files to gcs

    Args:
        destination_bucket (_type_): destination bucket
        prefix (_type_): the prefix/folder for the file name
        pq_file (_type_): the parquet file name
        local_file (_type_): the local file name
    """
    gcs_hook.upload(
            bucket_name=destination_bucket,
            object_name=f'{prefix}/{pq_file}',
            filename=local_file,
            mime_type='application/octet-stream',
            gzip=False,
    )
    
def upload_players_to_gcs(FILE_PATH, destination_bucket):
    """upload players to gcs

    Args:
        FILE_PATH (_type_): the path to the data files
        destination_bucket (_type_): the destination bucket
    """
    print('Uploading players to GCS')
    run_gcs_task(destination_bucket, PLAYERS_TABLE, 'atp_players.parquet', f'{FILE_PATH}/players/atp_players_transformed.parquet')
    print('Players uploaded to GCS')
    
def upload_matches_to_gcs(FILE_PATH, destination_bucket, MATCH_YEARS):
    """upload matches to gcs

    Args:
        FILE_PATH (_type_): the path to the data files
        destination_bucket (_type_): the destination bucket
        MATCH_YEARS (_type_): a list of years to load
    """
    print(f'Uploading matches to GCS')
    for match in MATCH_YEARS:
        run_gcs_task(destination_bucket, MATCHES_TABLE, f'atp_matches_{match}.parquet', f'{FILE_PATH}/matches/atp_matches_{match}_transformed.parquet')
    print(f'Matches uploaded to GCS')
    
def upload_rankings_to_gcs(FILE_PATH, destination_bucket, RANKING_YEARS):
    """ upload rankings to gcs

    Args:
        FILE_PATH (_type_): the path to the data files
        destination_bucket (_type_): the destination bucket
        RANKING_YEARS (_type_): a list of years to load
    """
    print(f'Uploading rankings to GCS')
    for rank in RANKING_YEARS:
        run_gcs_task(destination_bucket, RANKINGS_TABLE, f'atp_rankings_{rank}.parquet', f'{FILE_PATH}/rankings/atp_rankings_{rank}_transformed.parquet')
    print(f'Rankings uploaded to GCS')