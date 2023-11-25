{{
  config(
    materialized = 'table',
    )
}}

with all_matches as (

    select * from {{ ref('int_tournament_matches') }}

),
tournaments as (

    select * from {{ ref('int_tournaments') }}

),
players as (

    select * from {{ ref('stg_players') }}

),
stats as (

    select * from {{ ref('int_match_stats') }}

),
surfaces as (

    select * from {{ ref('int_surfaces') }}

)

SELECT
  match_id, tournaments.tourney_id, round, surface_name, all_matches.match_date, winner_id as winner, loser_id as loser, score, minutes FROM all_matches
    LEFT JOIN tournaments USING (tourney_id)
    LEFT JOIN surfaces ON (tournaments.surface = surfaces.surface_name)
    LEFT JOIN stats USING (match_id)
    LEFT JOIN players p1 ON (winner_id = p1.player_id)
    LEFT JOIN players p2 ON (loser_id = p2.player_id)
    WHERE tournaments.draw_size != 128
