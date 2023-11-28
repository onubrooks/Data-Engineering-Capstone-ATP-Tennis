# Data Modelling with Data Build Tool(DBT)

## Architecture

<img width="1185" alt="dbt_lineage" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/cf1e3a34-91ea-49a1-b7d3-20a2592ec7b6">


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

### Questions we can ask of these fact tables

**Match-related questions:**

1. How many matches have been played in each Grand Slam tournament?
2. What is the average match duration for each Grand Slam tournament?
3. How many matches have been played in each round of each Grand Slam tournament?
4. What is the average number of games played per match in each Grand Slam tournament?
5. What is the average number of sets played per match in each Grand Slam tournament?

**Player-related questions:**

1. Who has played the most Grand Slam matches?
2. Who has won the most Grand Slam matches?
3. Who has the highest winning percentage in Grand Slam matches?
4. Who has the most Grand Slam match wins against different opponents?
5. Who has the most Grand Slam match wins in different countries?

**Tournament-related questions:**

1. Which Grand Slam tournament has hosted the most matches?
2. Which Grand Slam tournament has had the longest matches?
3. Which Grand Slam tournament has had the most upsets (lower-ranked player wins over a higher-ranked player)?
4. Which Grand Slam tournament has had the most comebacks (player loses the first set and wins the match)?
5. Which Grand Slam tournament has had the highest attendance?

These are just a few examples of the many analytics questions you can ask of the facts tables we generated in this project. The specific questions you ask will depend on your specific interests and goals.

### Star Schema Modelling

Below are the diagrams for a star schema model of the transformed dataset. It is worth noting that the models in the metrics folder don't particularly follow the star schema and are designed as self-contained, denormalised analytics tables containing the full information with no need for joining other tables which can affect query performance. The approach to use between star schema or other models that use fully denormalised tables is a long discussion and really depends on the particular use case.

Grandslam Matches

<img width="735" alt="Grandslam Matches" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/dc22eaed-eea2-4289-a6fc-7b266fb4053e">


Tournament Winners

<img width="627" alt="Tournament Winners" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/9fc38ac8-c25b-46e1-93f4-b0806b14a54c">


Weekly Rankings

<img width="731" alt="Weekly Rankings" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/51fb65f0-5eb9-4184-8ed1-22856f9ff3af">


Match Advanced Stats

<img width="625" alt="Match Advanced Stats" src="https://github.com/onubrooks/Data-Engineering-Capstone-ATP-Tennis/assets/26160845/5661eac4-d93e-4298-9b97-796706e3187a">

