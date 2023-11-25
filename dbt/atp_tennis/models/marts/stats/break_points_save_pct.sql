WITH winner_break_points AS (
    SELECT winner_id, w_bpfaced, w_bpsaved
    FROM {{ ref('match_advanced_stats') }}
    WHERE w_1sw_bpfacedtin IS NOT NULL AND w_bpsaved IS NOT NULL
)

SELECT 
    wbp.winner_id,
    concat(p.first_name, ' ', p.last_name) as player_name, 
    wbp.w_bpfaced, 
    wbp.w_bpsaved, 
    (wbp.w_bpsaved / wbp.w_bpfaced) * 100 AS first_serve_percentage
FROM winner_break_points wbp
LEFT JOIN players p ON wbp.winner_id = p.player_id
