{{
  config(
    materialized = 'table',
    )
}}

WITH winner_break_points AS (
    SELECT winner_id, w_bpfaced, w_bpsaved
    FROM {{ ref('fact_match_advanced_stats') }}
    WHERE w_bpfaced IS NOT NULL AND w_bpsaved IS NOT NULL
),
players AS (
    SELECT player_id, first_name, last_name
    FROM {{ ref('stg_players') }}
)

SELECT 
    wbp.winner_id as player_id,
    concat(p.first_name, ' ', p.last_name) as player_name, 
    wbp.w_bpfaced as bp_faced, 
    wbp.w_bpsaved as bp_saved, 
    CASE 
        WHEN wbp.w_bpfaced = 0 THEN 0 
        ELSE (wbp.w_bpsaved / wbp.w_bpfaced) * 100 
    END AS bp_save_pct
FROM winner_break_points wbp
LEFT JOIN players p ON wbp.winner_id = p.player_id
