from transform.transform_tasks import transform_players_to_parquet, transform_matches_to_parquet, transform_rankings_to_parquet

def transform_tennis_data(FILE_SAVE_LOCATION, MATCH_YEARS, RANK_YEARS):
    print('Transforming tennis data')
    transform_players_to_parquet(FILE_SAVE_LOCATION)
    transform_matches_to_parquet(FILE_SAVE_LOCATION, MATCH_YEARS)
    transform_rankings_to_parquet(FILE_SAVE_LOCATION, RANK_YEARS)
    print('Tennis data transformed and saved to parquet')