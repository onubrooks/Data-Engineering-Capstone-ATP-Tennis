import os
import pandas as pd

from load_db import create_db_table, insert_into_db, get_db_conn_engine
from load_functions import get_country_name, str_to_datetime

PG_HOST = "127.0.0.1" #"altschool_de" #pgdatabase
PG_USER ="postgres"
PG_PASSWORD = ""
PG_PORT = 5432
PG_DATABASE = "atp_tennis_2000_2019"

def clean_and_load_players(db_engine):
    # load player file and examine the data
    players = pd.read_parquet('downloads/players/atp_players.parquet')
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
    players.to_parquet('downloads/players/atp_players_transformed.parquet')
    create_db_table(db_engine, 'atp_players', players)
    insert_into_db(db_engine, 'atp_players', players)


def clean_and_load_matches(db_engine, match_years):
    # load all matches file and examine the data, then write transformed data to parquet
    for index, year in enumerate(match_years):
        matches = pd.read_parquet(f'downloads/matches/atp_matches_{year}.parquet')
        # drop columns winner_ht, loser_ht, winner_name, winner_ioc, loser_name, loser_ioc
        matches = matches.drop(columns=['winner_ht', 'loser_ht', 'winner_name', 'winner_ioc', 'loser_name', 'loser_ioc'])
        # convert tourney_date to datetime from yyyymmdd format
        matches = matches.rename(columns={'tourney_date': 'match_date'})
        matches['match_date'] = matches['match_date'].astype(str).str.slice(0, 8)
        matches['match_date'] = matches.match_date.apply(str_to_datetime)
        
        # write transformed matches file back to parquet and postgres
        matches.reset_index(drop=True, inplace=True)
        matches.to_parquet(f'downloads/matches/atp_matches_{year}_transformed.parquet')
        if index == 0:
            create_db_table(db_engine, f'atp_matches', matches)
        insert_into_db(db_engine, f'atp_matches', matches)

def clean_and_load_rankings(db_engine, rank_years):
    # load rankings file and examine the data, then write transformed data to parquet using enumerate
    for index, year in enumerate(rank_years):
        rankings = pd.read_parquet(f'downloads/rankings/atp_rankings_{year}.parquet')
        # convert ranking_date to datetime from yyyymmdd format
        rankings['ranking_date'] = rankings['ranking_date'].astype(str).str.slice(0, 8)
        rankings['ranking_date'] = rankings.ranking_date.apply(str_to_datetime)
        
        # write transformed rankings file back to parquet and postgres
        rankings.reset_index(drop=True, inplace=True)
        rankings.to_parquet(f'downloads/rankings/atp_rankings_{year}_transformed.parquet')
        if index == 0:
            create_db_table(db_engine, f'atp_rankings', rankings)
        insert_into_db(db_engine, f'atp_rankings', rankings)
