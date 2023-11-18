from transform.transform_functions import convert_to_parquet

def transform_players_to_parquet(FILE_SAVE_LOCATION):
    # convert atp players file to parquet
    csv_file = f'{FILE_SAVE_LOCATION}/players/atp_players.csv'
    parquet_file = f'{FILE_SAVE_LOCATION}/players/atp_players.parquet'
    convert_to_parquet(csv_file, parquet_file)

def transform_matches_to_parquet(FILE_SAVE_LOCATION, MATCH_YEARS):
    for year in MATCH_YEARS:
        csv_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.csv'
        parquet_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.parquet'
        convert_to_parquet(csv_file, parquet_file)
        print(f'Converted {csv_file} to {parquet_file}')

def transform_rankings_to_parquet(FILE_SAVE_LOCATION, RANK_YEARS):
    for year in RANK_YEARS:
        csv_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.csv'
        parquet_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.parquet'
        convert_to_parquet(csv_file, parquet_file)
        print(f'Converted {csv_file} to {parquet_file}')