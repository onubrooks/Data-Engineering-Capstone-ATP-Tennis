{{
  config(
    materialized = 'table',
    )
}}

with match_stats as (

    select * from {{ ref('int_match_stats') }}

),
players as (
    
        select * from {{ ref('stg_players') }}
    
),
matches as (

    select * from {{ ref('int_tournament_matches') }}

)

SELECT
    matches.match_id,
    winner_id,
    loser_id,
    w_ace,
    w_df,
    w_svpt,
    w_1stin,
    w_1stwon,
    w_2ndwon,
    w_svgms,
    w_bpsaved,
    w_bpfaced,
    l_ace,
    l_df,
    l_svpt,
    l_1stin,
    l_1stwon,
    l_2ndwon,
    l_svgms,
    l_bpsaved,
    l_bpfaced
FROM match_stats
    left join matches on match_stats.match_id = matches.match_id
    left join players p1 on matches.winner_id = p1.player_id
    left join players p2 on matches.loser_id = p2.player_id
    