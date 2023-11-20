from transform.transform_functions import convert_to_parquet

def transform_players_to_parquet(FILE_SAVE_LOCATION):
    """transform players csv to parquet format

    Args:
        FILE_SAVE_LOCATION (_type_): the path to the data files
    """
    # convert atp players file to parquet
    csv_file = f'{FILE_SAVE_LOCATION}/players/atp_players.csv'
    parquet_file = f'{FILE_SAVE_LOCATION}/players/atp_players.parquet'
    convert_to_parquet(csv_file, parquet_file)

def transform_matches_to_parquet(FILE_SAVE_LOCATION, MATCH_YEARS):
    """transform matches csv to parquet format

    Args:
        FILE_SAVE_LOCATION (_type_): the path to the data files
        MATCH_YEARS (_type_): a list of years to load
    """
    for year in MATCH_YEARS:
        csv_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.csv'
        parquet_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.parquet'
        convert_to_parquet(csv_file, parquet_file)
        print(f'Converted {csv_file} to {parquet_file}')

def transform_rankings_to_parquet(FILE_SAVE_LOCATION, RANK_YEARS):
    """transform rankings csv to parquet format

    Args:
        FILE_SAVE_LOCATION (_type_): the path to the data files
        RANK_YEARS (_type_): a list of years to load
    """
    for year in RANK_YEARS:
        csv_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.csv'
        parquet_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.parquet'
        convert_to_parquet(csv_file, parquet_file)
        print(f'Converted {csv_file} to {parquet_file}')