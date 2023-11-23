with all_matches as (

    select * from {{ ref('stg_matches') }}

)

SELECT
    -- concat tourney_id and match_num to create a unique id for each match, use as primary key
    concat(tourney_id, match_num) AS match_id,
    tourney_id, 
    DATE(match_date) AS match_date,
    match_num,
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
    l_bpfaced,
    winner_rank,
    winner_rank_points,
    loser_rank,
    loser_rank_points
FROM all_matches