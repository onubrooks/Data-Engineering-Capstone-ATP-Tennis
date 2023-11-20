from load.load_tasks import clean_and_load_players, clean_and_load_matches, clean_and_load_rankings
from load.load_gcp_tasks import upload_players_to_gcs, upload_matches_to_gcs, upload_rankings_to_gcs
from load.load_db import get_db_conn_engine

def clean_and_load_tennis_data(FILE_PATH, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE, MATCH_YEARS, RANK_YEARS):
    """clean and load tennis data to parquet and postgres

    Args:
        FILE_PATH (_type_): the path to the data files
        PG_USER (_type_): the postgres user
        PG_PASSWORD (_type_): the postgres password
        PG_HOST (_type_): the postgres host
        PG_PORT (_type_): the postgres port
        PG_DATABASE (_type_): the postgres database
        MATCH_YEARS (_type_): the years to load for matches
        RANK_YEARS (_type_): the years to load for rankings
    """
    db_engine = get_db_conn_engine(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    
    print('Cleaning and loading tennis data')
    clean_and_load_players(FILE_PATH, db_engine)
    clean_and_load_matches(FILE_PATH, db_engine, MATCH_YEARS)
    clean_and_load_rankings(FILE_PATH, db_engine, RANK_YEARS)
    print('Tennis data cleaned and loaded to parquet and postgres')
    
    
def upload_tennis_data_to_gcs(FILE_PATH, destination_bucket, MATCH_YEARS, RANK_YEARS):
    """upload tennis data to gcs

    Args:
        FILE_PATH (_type_): the path to the data files
        destination_bucket (_type_): the destination bucket
        MATCH_YEARS (_type_): the years to load for matches
        RANK_YEARS (_type_): the years to load for rankings
    """
    print('Uploading tennis data to GCS')
    # Upload players parquet file to gcs
    upload_players_to_gcs(FILE_PATH, destination_bucket)
    # Upload matches to gcs
    upload_matches_to_gcs(FILE_PATH, destination_bucket, MATCH_YEARS)
    # Upload rankings to gcs
    upload_rankings_to_gcs(FILE_PATH, destination_bucket, RANK_YEARS)
    print('Tennis data uploaded to GCS')
    