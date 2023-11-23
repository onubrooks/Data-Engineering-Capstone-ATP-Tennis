with weeks as (

    select * from {{ ref('weeks') }}

),
rankings as (

    select * from {{ ref('atp_rankings') }}

),
players as (

    select * from {{ ref('atp_players') }}

)

SELECT
  week_id, rank, concat(first_name, ' ', last_name) as player_name, player_id, points
FROM weeks inner join rankings on weeks.week_date = rankings.ranking_date
inner join players on rankings.player = players.player_id
