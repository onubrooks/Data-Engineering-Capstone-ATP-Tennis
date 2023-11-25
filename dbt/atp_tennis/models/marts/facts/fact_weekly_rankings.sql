{{
  config(
    materialized = 'table',
    )
}}

with weeks as (

    select * from {{ ref('int_weeks') }}

),
rankings as (

    select * from {{ ref('stg_rankings') }}

),
players as (

    select * from {{ ref('stg_players') }}

)

SELECT
  week_id, 
  rank, 
  concat(first_name, ' ', last_name) as player_name, 
  player_id, 
  points
FROM weeks inner join rankings on weeks.week_date = rankings.ranking_date
inner join players on rankings.player = players.player_id
