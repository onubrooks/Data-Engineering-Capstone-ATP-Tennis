{{
  config(
    materialized = 'table',
    )
}}

WITH player_weeks AS (
    SELECT
        player_id,
        player_name,
        COUNT(*) AS total_weeks_as_number_one
    FROM {{ ref('fact_weekly_rankings') }}
    WHERE rank = 1
    GROUP BY player_id, player_name
)

SELECT
    player_id,
    player_name,
    total_weeks_as_number_one
FROM player_weeks
ORDER BY total_weeks_as_number_one DESC
