{{
  config(
    materialized = 'table',
    )
}}

SELECT
  player_id,
  week_id,
  points,
  AVG(points) OVER (
    PARTITION BY player_id
    ORDER BY week_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS rolling_average_points
FROM {{ ref('fact_weekly_rankings') }}
