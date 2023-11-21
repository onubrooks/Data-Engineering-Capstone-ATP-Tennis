with source as (

    select * from {{ source('atp_tennis_data', 'atp_rankings') }}

),

atp_rankings as (

    select
        ranking_date,
        rank,
        player,
        points

    from source

)

select * from atp_rankings