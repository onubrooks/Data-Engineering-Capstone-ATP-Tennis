with source as (

    select * from {{ source('atp_tennis_data', 'atp_players') }}

),

atp_players as (

    select
        player_id,
        first_name,
        last_name,
        hand,
        dob,
        country_code,
        height,
        birth_date,
        country

    from source

)

select * from atp_players