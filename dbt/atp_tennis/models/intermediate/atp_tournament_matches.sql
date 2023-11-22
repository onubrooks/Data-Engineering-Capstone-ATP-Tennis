-- generate a model for tennis surfaces in sql from the tennis_matches table
with all_matches as (

    select * from {{ ref('atp_matches') }}

)

SELECT
    concat(tourney_id, match_num) AS match_id,
    tourney_id, 
    DATE(match_date) AS match_date,
    match_num,
    winner_id,
    winner_seed,
    winner_entry,
    winner_hand,
    winner_age,
    loser_id,
    loser_seed,
    loser_entry,
    loser_hand,
    loser_age,
    score,
    best_of,
    round,
    minutes
FROM all_matches