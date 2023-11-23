with source as (

    select * from {{ source('atp_tennis_data', 'atp_rankings') }}

),

atp_rankings as (

    select
        DATE(ranking_date) AS ranking_date,
        rank,
        player,
        points

    from source

)

select * from atp_rankings