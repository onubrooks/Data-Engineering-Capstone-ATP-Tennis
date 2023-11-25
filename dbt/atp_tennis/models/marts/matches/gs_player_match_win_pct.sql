-- Calculate the total number of matches played by each player
WITH player_matches AS (
    SELECT
        player_id,
        COUNT(*) AS total_matches
    FROM
        {{ ref('grandslam_matches') }}
    GROUP BY
        player_id
),

-- Calculate the total number of matches won by each player
player_wins AS (
    SELECT
        winner AS player_id,
        COUNT(*) AS total_wins
    FROM
        {{ ref('grandslam_matches') }}
    GROUP BY
        player_id
),

-- Calculate the player match win percentage
player_match_win_pct AS (
    SELECT
        pm.player_id,
        concat(p.first_name, ' ', p.last_name) AS player_name,
        pm.total_matches,
        pw.total_wins,
        CASE
            WHEN pm.total_matches > 0 THEN pw.total_wins / pm.total_matches::float * 100
            ELSE 0
        END AS win_percentage
    FROM
        player_matches pm
    LEFT JOIN
        player_wins pw ON pm.player_id = pw.player_id
    LEFT JOIN
        {{ ref('stg_players') }} p ON pm.player_id = p.player_id
)

SELECT
    player_id,
    player_name,
    total_matches,
    total_wins,
    win_percentage
FROM
    player_match_win_pct
ORDER BY
    win_percentage DESC;
