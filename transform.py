import pandas as pd
import pycountry

from postgres import create_db_table, insert_into_db, get_db_conn_engine

def print_df(df):
    print(df.head())

def get_country_name(code):
    try:
        return pycountry.countries.get(alpha_3=code).name
    except:
        try:
            return pycountry.historic_countries.get(alpha_3=code).name
        except:
            return None
        
def str_to_datetime(x):
    if pd.isnull(x):
        return None
    else:
        try:
            return pd.to_datetime(x, format='%Y%m%d')
        except:
            return None

PG_HOST = "127.0.0.1" #"altschool_de" #pgdatabase
PG_USER ="postgres"
PG_PASSWORD = ""
PG_PORT = 5432
PG_DATABASE = "atp_tennis_2000_2019"

db_engine = get_db_conn_engine(PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DATABASE)
match_years=(2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019)
rank_years=('00s', '10s', '20s')

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
