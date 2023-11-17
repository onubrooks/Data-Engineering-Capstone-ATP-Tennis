from load_tasks import clean_and_load_players, clean_and_load_matches, clean_and_load_rankings
from load_gcp_tasks import upload_players_to_gcs, upload_matches_to_gcs, upload_rankings_to_gcs
from load_functions import get_db_conn_engine

def clean_and_load_tennis_data(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE, MATCH_YEARS, RANK_YEARS):
    db_engine = get_db_conn_engine(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    
    print('Cleaning and loading tennis data')
    clean_and_load_players(db_engine)
    clean_and_load_matches(db_engine, MATCH_YEARS)
    clean_and_load_rankings(db_engine, RANK_YEARS)
    print('Tennis data cleaned and loaded to parquet and postgres')
    
    
def upload_tennis_data_to_gcs(destination_bucket, MATCH_YEARS, RANK_YEARS):
    print('Uploading tennis data to GCS')
    # Upload players parquet file to gcs
    upload_players_to_gcs(destination_bucket)
    # Upload matches to gcs
    upload_matches_to_gcs(destination_bucket, MATCH_YEARS)
    # Upload rankings to gcs
    upload_rankings_to_gcs(destination_bucket, RANK_YEARS)
    print('Tennis data uploaded to GCS')
    