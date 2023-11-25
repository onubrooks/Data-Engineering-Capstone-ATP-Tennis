{{
  config(
    materialized = 'table',
    )
}}

WITH matches as (

    SELECT * from {{ ref('int_tournament_matches') }} 

),
players as (

    SELECT * from {{ ref('stg_players') }}

),
tournaments as (

    SELECT * from {{ ref('int_tournaments') }}

)

SELECT 
    tourney_id, 
    EXTRACT(YEAR FROM match_date) AS year, 
    concat(first_name, ' ', last_name) AS winner, 
    winner_id, 
    winner_seed,
    winner_age
FROM matches
    LEFT JOIN tournaments USING (tourney_id)
    LEFT JOIN players ON winner_id = player_id