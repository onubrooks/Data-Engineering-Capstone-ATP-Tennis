# Data Modelling with Data Build Tool(DBT)

Two important handy commands DBT provides are:
To generate base model SQL:

```sh
dbt run-operation generate_base_model --args '{"source_name": "atp_tennis_data", "table_name": "atp_players"}'
```

To generate base model YAML files:

```sh
dbt run-operation generate_model_yaml --args '{"model_names": ["atp_players", "atp_rankings", "atp_matches"]}'
```

## Architecture

### Tables vs Views

For best practices, we use views for all staging and intermediate models since they occupy less space and need to be up to date at all times. The marts however are actual tables on BigQuery so that analytics queries can be run quickly and on demand.

### Staging Models

The staging models are the first step in the modelling process. They are responsible for cleaning and preparing the data from the source systems before it is loaded into the downstream models. In this case, there are three staging models:

* **stg_players:** This model contains information about all of the players on the ATP tour. It includes columns for the player's ID, name, nationality, height, weight, and hand.
* **stg_rankings:** This model contains information about the rankings of all of the players on the ATP tour. It includes columns for the player's ID, rank, rank points, and date.
* **stg_matches:** This model contains information about all of the matches on the ATP tour. It includes columns for the match's ID, date, tournament ID, winner ID, loser ID, score, and best of.

### Intermediate Models

The intermediate models are used to transform the data from the staging models into a form that is more useful for the downstream models. In this case, there are five intermediate models:

* **int_surfaces:** This model contains a list of all of the tennis surfaces on the ATP tour. It includes columns for the surface's ID and name.
* **int_tournaments:** This model contains a list of all of the tennis tournaments on the ATP tour. It includes columns for the tournament's ID, name, surface, level, draw size, location, country, prize money, and currency.
* **int_tournament_matches:** This model contains a list of all of the matches on the ATP tour that are associated with a tournament. It includes columns for the match's ID, tournament ID, date, match number, winner ID, winner seed, winner entry, winner hand, winner age, loser ID, loser seed, loser entry, loser hand, loser age, score, best of, and round.
* **int_match_stats:** This model contains statistics about all of the matches on the ATP tour. It includes columns for the match's ID, tournament ID, date, match number, winner's aces, winner's double faults, winner's service points played, winner's first serves in, winner's first serve points won, winner's second serve points won, winner's service games played, winner's break points saved, winner's break points faced, loser's aces, loser's double faults, loser's service points played, loser's first serves in, loser's first serve points won, loser's second serve points won, loser's service games played, loser's break points saved, loser's break points faced, winner's rank, winner's rank points, loser's rank, and loser's rank points.
* **int_weeks:** This model contains a list of all of the weeks on the ATP tour. It includes columns for the week's ID, date, year, and week number.

### Mart Models

The mart models are the final step in the transformation process. They are used to aggregate and summarize the data from the upstream models in a way that is easy to analyze and report on. In this case, there are two categories modelled:

* **Fact Tables:** These tables contain the raw data from the upstream models. They are used to answer questions about specific events or transactions. In this case, there are five fact tables:
  * **fact_grandslam_matches:** This table contains information about all of the matches played in Grand Slam tournaments.
  * **fact_match_advanced_stats:** This table contains additional statistics about all of the matches on the ATP tour.
  * **fact_non_grandslam_matches:** This table contains information about all of the matches played in non-Grand Slam tournaments.
  * **fact_tournament_winners:** This table contains information about the winners of all of the tournaments on the ATP tour.
  * **fact_weekly_rankings:** This table contains information about the rankings of all of the players on the ATP tour at the end of each week.

* **Metrics Tables:** These tables contain aggregated metrics that are calculated from the data in the fact tables. They are used to answer questions about trends and patterns in the data. In this case, there are six metrics tables:
  * **metric_grandslam_player_match_win_pct:** This table contains the match win percentage for each player in Grand Slam tournaments.
  * **metric_player_match_win_pct:** This table contains the match win percentage for each player in all tournaments.
  * **metric_rolling_avg_points:** This table contains the rolling average of rank points for each player.
  * **metric_weeks_as_number_one:** This table contains the number of weeks
