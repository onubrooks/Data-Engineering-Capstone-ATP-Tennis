import pandas as pd

from load.load_db import create_db_table, insert_into_db
from load.load_functions import get_country_name, str_to_datetime

def clean_and_load_players(FILE_PATH, db_engine):
    """load player file and examine the data, then write transformed data to parquet

    Args:
        FILE_PATH (_type_): the path to the data files
        db_engine (_type_): the database engine
    """
    # load player file and examine the data
    players = pd.read_parquet(f'{FILE_PATH}/players/atp_players.parquet')
    # drop wikidata_id column
    players = players.drop(columns=['wikidata_id'])
    # convert dob to string and slice to get yymmdd format
    players['dob'] = players['dob'].astype(str).str.slice(0, 8)
    # convert dob to date from yymmdd format
    players['birth_date'] = players['dob'].apply(str_to_datetime)
    # convert hand to category
    players.hand = players.hand.astype('category')
    # rename ioc, name_first and name_last columns to country_code, first_name and last_name
    players = players.rename(columns={'ioc': 'country_code', 'name_first': 'first_name', 'name_last': 'last_name'})
    # map country codes to country names
    players['country'] = players.country_code.apply(get_country_name)
    # print unique country codes with no country name
    print(players[players.country.isnull()].country_code.unique())
    players.reset_index(drop=True, inplace=True)

    # write transformed players file back to parquet and postgres
    players.to_parquet(f'{FILE_PATH}/players/atp_players_transformed.parquet')
    create_db_table(db_engine, 'atp_players', players)
    insert_into_db(db_engine, 'atp_players', players)


def clean_and_load_matches(FILE_PATH, db_engine, match_years):
    """load all matches file and examine the data, then write transformed data to parquet

    Args:
        FILE_PATH (_type_): the path to the data files
        db_engine (_type_): the database engine
        match_years (_type_): a list of years to load
    """
    for index, year in enumerate(match_years):
        matches = pd.read_parquet(f'{FILE_PATH}/matches/atp_matches_{year}.parquet')
        # drop columns winner_ht, loser_ht, winner_name, winner_ioc, loser_name, loser_ioc
        matches = matches.drop(columns=['winner_ht', 'loser_ht', 'winner_name', 'winner_ioc', 'loser_name', 'loser_ioc'])
        # convert tourney_date to datetime from yyyymmdd format
        matches = matches.rename(columns={'tourney_date': 'match_date'})
        matches['match_date'] = matches['match_date'].astype(str).str.slice(0, 8)
        matches['match_date'] = matches.match_date.apply(str_to_datetime)
        
        # write transformed matches file back to parquet and postgres
        matches.reset_index(drop=True, inplace=True)
        matches.to_parquet(f'{FILE_PATH}/matches/atp_matches_{year}_transformed.parquet')
        if index == 0:
            create_db_table(db_engine, f'atp_matches', matches)
        insert_into_db(db_engine, f'atp_matches', matches)

def clean_and_load_rankings(FILE_PATH, db_engine, rank_years):
    """load rankings file and examine the data, then write transformed data to parquet using enumerate

    Args:
        FILE_PATH (_type_): the path to the data files
        db_engine (_type_): the database engine
        rank_years (_type_): a list of years to load
    """
    for index, year in enumerate(rank_years):
        rankings = pd.read_parquet(f'{FILE_PATH}/rankings/atp_rankings_{year}.parquet')
        # convert ranking_date to datetime from yyyymmdd format
        rankings['ranking_date'] = rankings['ranking_date'].astype(str).str.slice(0, 8)
        rankings['ranking_date'] = rankings.ranking_date.apply(str_to_datetime)
        
        # write transformed rankings file back to parquet and postgres
        rankings.reset_index(drop=True, inplace=True)
        rankings.to_parquet(f'{FILE_PATH}/rankings/atp_rankings_{year}_transformed.parquet')
        if index == 0:
            create_db_table(db_engine, f'atp_rankings', rankings)
        insert_into_db(db_engine, f'atp_rankings', rankings)
