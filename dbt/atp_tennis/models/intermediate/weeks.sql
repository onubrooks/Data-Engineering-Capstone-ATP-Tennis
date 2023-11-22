with ranking_table as (

    select DISTINCT ranking_date from {{ ref('atp_rankings') }}

)

SELECT
  concat(EXTRACT(YEAR FROM ranking_date), '-W-', EXTRACT(WEEK FROM ranking_date)) AS week_id,
  EXTRACT(YEAR FROM ranking_date) AS year,
  EXTRACT(WEEK FROM ranking_date) AS week_number,
  ranking_date AS week_date
FROM ranking_table
