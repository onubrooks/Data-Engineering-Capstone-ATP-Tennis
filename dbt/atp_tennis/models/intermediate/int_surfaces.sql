-- generate a model for tennis surfaces in sql from the tennis_matches table
with all_matches as (

    select DISTINCT surface from {{ ref('stg_matches') }}

)

SELECT
  ROW_NUMBER() OVER (ORDER BY surface) AS surface_id,
  surface AS surface_name
FROM all_matches
WHERE surface IS NOT NULL