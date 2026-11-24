SELECT id,
       game_date,
       home_team,
       away_team,
       home_score,
       away_score,
       home_win,
       external_game_id,
       season,
       week,
       game_tie
FROM public.games
LIMIT 1000;


SELECT *
FROM public.games
WHERE season = 2026