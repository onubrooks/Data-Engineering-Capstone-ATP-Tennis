{{
	config(
		partition_by={
			"field":"match_date",
			"data_type": "date_time",
			"granularity": "year"
		}
	)
}}

with source as (

    select * from {{ source('atp_tennis_data', 'atp_matches') }}

),

atp_matches as (

    select
        tourney_id,
        tourney_name,
        surface,
        draw_size,
        tourney_level,
        DATE(match_date) AS match_date,
        match_num,
        winner_id,
        winner_seed,
        winner_entry,
        winner_hand,
        winner_age,
        loser_id,
        loser_seed,
        loser_entry,
        loser_hand,
        loser_age,
        score,
        best_of,
        round,
        minutes,
        w_ace,
        w_df,
        w_svpt,
        w_1stin,
        w_1stwon,
        w_2ndwon,
        w_svgms,
        w_bpsaved,
        w_bpfaced,
        l_ace,
        l_df,
        l_svpt,
        l_1stin,
        l_1stwon,
        l_2ndwon,
        l_svgms,
        l_bpsaved,
        l_bpfaced,
        winner_rank,
        winner_rank_points,
        loser_rank,
        loser_rank_points

    from source

)

select * from atp_matches