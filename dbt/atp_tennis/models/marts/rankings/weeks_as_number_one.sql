-- This query calculates the total number of weeks each player has been ranked as number one
-- and orders the result in descending order

WITH player_weeks AS (
    SELECT
        player_id,
        player_name,
        SUM(weeks_as_number_one) AS total_weeks_as_number_one
    FROM {{ ref('weekly_rankings') }}
    GROUP BY player_id, player_name
)

SELECT
    player_id,
    player_name,
    total_weeks_as_number_one
FROM player_weeks
ORDER BY total_weeks_as_number_one DESC;
