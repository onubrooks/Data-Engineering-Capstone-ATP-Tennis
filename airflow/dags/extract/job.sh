#!/bin/bash

# Access parameters passed from the DAG
# base_url="{{ params.base_url }}"
# download_directory="{{ params.download_directory }}"
base_url=$1
download_directory=$2

# Create the downloads directory if it doesn't exist
mkdir -p $download_directory/matches
mkdir -p $download_directory/rankings
mkdir -p $download_directory/players

#!/bin/bash

# Download the players file
player_url="${base_url}atp_players.csv"
wget -O "${download_directory}/players/atp_players.csv" "${player_url}"

<<comment
# Specify the years to download data for
match_years=(2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019 2020)

# Download match data for each year
for year in "${match_years[@]}"; do
    # Construct the URL for the current year's data file
    match_url="${base_url}atp_matches_${year}.csv"

    # Download the match files
    wget -O "${download_directory}/matches/atp_matches_${year}.csv" "${match_url}"
done

# Download ranking data for each decade
rank_years=(00s 10s 20s)

for year in "${rank_years[@]}"; do
    # Construct the URL for the current year's data file
    rank_url="${base_url}atp_rankings_${year}.csv"

    # Download the match files
    wget -O "${download_directory}/rankings/atp_rankings_${year}.csv" "${rank_url}"
done
comment

# To test, run: sh download_files.sh https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/ downloads
