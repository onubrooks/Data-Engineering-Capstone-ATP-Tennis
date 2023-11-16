import os
import pyarrow.csv as pv
import pyarrow.parquet as pq
from datetime import datetime

def convert_to_parquet(csv_file, parquet_file):
    if not csv_file.endswith('csv'):
        raise ValueError('The input file is not in csv format')
    
    print(f'Reading {csv_file}')
    table=pv.read_csv(os.path.abspath(csv_file))
    print(f'Writing {parquet_file}')
    pq.write_table(table, parquet_file)

FILE_SAVE_LOCATION = "downloads"   
# convert atp players file to parquet
csv_file = f'{FILE_SAVE_LOCATION}/players/atp_players.csv'
parquet_file = f'{FILE_SAVE_LOCATION}/players/atp_players.parquet'
convert_to_parquet(csv_file, parquet_file)
    
match_years=(2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)

for year in match_years:
    csv_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.csv'
    parquet_file = f'{FILE_SAVE_LOCATION}/matches/atp_matches_{year}.parquet'
    convert_to_parquet(csv_file, parquet_file)
    print(f'Converted {csv_file} to {parquet_file}')
    
rank_years=('00s', '10s', '20s')
for year in rank_years:
    csv_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.csv'
    parquet_file = f'{FILE_SAVE_LOCATION}/rankings/atp_rankings_{year}.parquet'
    convert_to_parquet(csv_file, parquet_file)
    print(f'Converted {csv_file} to {parquet_file}')