with source as (

    select * from {{ source('atp_tennis_data', 'atp_players') }}

),

atp_players as (

    select
        player_id,
        first_name,
        last_name,
        hand,
        timestamp(dob) as dob,
        country_code,
        height,
        DATE(birth_date) as birth_date,
        country

    from source

)

select * from atp_players