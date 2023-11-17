from airflow.providers.google.cloud.hooks.gcs import GCSHook

gcs_hook = GCSHook(
    gcp_conn_id="google_cloud_default",
    delegate_to=None,
    impersonation_chain=None,
)
def run_gcs_task(destination_bucket, prefix, pq_file, local_file):
    gcs_hook.upload(
            bucket_name=destination_bucket,
            object_name=f'{prefix}/{pq_file}',
            filename=local_file,
            mime_type='application/octet-stream',
            gzip=False,
    )
    
def upload_players_to_gcs(destination_bucket):
    print('Uploading players to GCS')
    run_gcs_task(destination_bucket, 'players', 'atp_players.parquet', 'downloads/players/atp_players_transformed.parquet')
    print('Players uploaded to GCS')
    
def upload_matches_to_gcs(destination_bucket, MATCH_YEARS):
    print(f'Uploading matches to GCS')
    for match in MATCH_YEARS:
        run_gcs_task(destination_bucket, 'matches', f'atp_matches_{match}.parquet', f'downloads/matches/atp_matches_{match}_transformed.parquet')
    print(f'Matches uploaded to GCS')
    
def upload_rankings_to_gcs(destination_bucket, RANKING_YEARS):
    print(f'Uploading rankings to GCS')
    for rank in RANKING_YEARS:
        run_gcs_task(destination_bucket, 'rankings', f'atp_rankings_{rank}.parquet', f'downloads/rankings/atp_rankings_{rank}_transformed.parquet')
    print(f'Rankings uploaded to GCS')