-- Calculate rolling average of points for each player
SELECT
  player_id,
  week_id,
  points,
  AVG(points) OVER (
    PARTITION BY player_id
    ORDER BY week_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS rolling_average
FROM rankings;

-- Calculate standard deviation of points for each player
SELECT
  player_id,
  STDDEV(points) AS points_stddev
FROM rankings
GROUP BY player_id;

-- Identify players on hot streaks or cold streaks
SELECT
  player_id,
  week_id,
  points,
  AVG(points) OVER (
    PARTITION BY player_id
    ORDER BY week_id
    ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
  ) AS moving_average
FROM rankings;
