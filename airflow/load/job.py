from load_tasks import clean_and_load_players, clean_and_load_matches, clean_and_load_rankings
from load_gcp_tasks import upload_to_gcs
from load_functions import get_db_conn_engine

def clean_and_load_tennis_data(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE, MATCH_YEARS, RANK_YEARS):
    db_engine = get_db_conn_engine(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
    
    print('Cleaning and loading tennis data')
    clean_and_load_players(db_engine)
    clean_and_load_matches(db_engine, MATCH_YEARS)
    clean_and_load_rankings(db_engine, RANK_YEARS)
    print('Tennis data cleaned and loaded to parquet and postgres')
    
    

    