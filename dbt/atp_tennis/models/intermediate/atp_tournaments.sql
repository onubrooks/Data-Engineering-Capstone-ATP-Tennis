-- generate a model for tennis surfaces in sql from the tennis_matches table
with all_matches as (

    select * from {{ ref('atp_matches') }}

)

SELECT
  DISTINCT tourney_id, tourney_name, draw_size, tourney_level, surface
FROM all_matches