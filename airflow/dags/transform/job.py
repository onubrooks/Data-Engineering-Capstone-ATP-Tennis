from transform.transform_tasks import transform_players_to_parquet, transform_matches_to_parquet, transform_rankings_to_parquet

def transform_tennis_data(FILE_SAVE_LOCATION, MATCH_YEARS, RANK_YEARS):
    """transform tennis data from csv to parquet format

    Args:
        FILE_SAVE_LOCATION (_type_): the path to the data files
        MATCH_YEARS (_type_): the years to load for matches
        RANK_YEARS (_type_): the years to load for rankings
    """
    print('Transforming tennis data')
    transform_players_to_parquet(FILE_SAVE_LOCATION)
    transform_matches_to_parquet(FILE_SAVE_LOCATION, MATCH_YEARS)
    transform_rankings_to_parquet(FILE_SAVE_LOCATION, RANK_YEARS)
    print('Tennis data transformed and saved to parquet')