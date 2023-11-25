WITH winners_first_serve AS (
    SELECT winner_id, w_1stin, w_1stwon
    FROM {{ ref('match_advanced_stats') }}
    WHERE w_1stin IS NOT NULL AND w_1stwon IS NOT NULL
)

SELECT 
    wfs.winner_id, 
    concat(p.first_name, ' ', p.last_name) as player_name, 
    wfs.w_1stin, 
    wfs.w_1stwon, 
    (wfs.w_1stwon / wfs.w_1stin) * 100 AS first_serve_percentage
FROM winners_first_serve wfs
LEFT JOIN players p ON wfs.winner_id = p.player_id
