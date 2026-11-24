SELECT *
FROM games
LIMIT 10;

DELETE FROM games
WHERE season = 2026
AND status != 'STATUS_FINAL';

SELECT
    COUNT(*)
FROM games
WHERE season = 2026
AND tie = true;


DELETE FROM games
WHERE season = 2026
AND tie = true;


SELECT
    season,
    COUNT(*) as games
FROM games
WHERE season = 2026
GROUP BY season;

SELECT
    COUNT(*)
FROM games
WHERE season = 2026
AND game_tie = TRUE;

SELECT
    home_score,
    away_score,
    game_tie,
    home_win
FROM games
WHERE season = 2026
LIMIT 20;


SELECT COUNT(*)
FROM games
WHERE season = 2026;

SELECT COUNT(*)
FROM games
WHERE season = 2026
AND game_tie = TRUE;

SELECT
    week,
    home_team,
    away_team,
    home_score,
    away_score,
    game_tie
FROM games
WHERE season = 2026
AND game_tie = TRUE
ORDER BY week;

DELETE FROM games
WHERE season = 2026;