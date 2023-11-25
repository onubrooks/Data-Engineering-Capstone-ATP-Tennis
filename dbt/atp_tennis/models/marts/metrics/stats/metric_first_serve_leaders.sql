{{
  config(
    materialized = 'table',
    )
}}

WITH winners_first_serve AS (
    SELECT winner_id, w_1stin, w_1stwon
    FROM {{ ref('fact_match_advanced_stats') }}
    WHERE w_1stin IS NOT NULL AND w_1stwon IS NOT NULL
),
players AS (
    SELECT player_id, first_name, last_name
    FROM {{ ref('stg_players') }}
)

SELECT 
    wfs.winner_id as player_id, 
    concat(p.first_name, ' ', p.last_name) as player_name, 
    wfs.w_1stin as first_serve_in, 
    wfs.w_1stwon as first_serve_won, 
    CASE 
        WHEN wfs.w_1stin = 0 THEN 0 
        ELSE (wfs.w_1stwon / wfs.w_1stin) * 100 
    END AS first_serve_pct
FROM winners_first_serve wfs
LEFT JOIN players p ON wfs.winner_id = p.player_id
ORDER BY first_serve_pct DESC
