SELECT
    game_date,
    season,
    week,
    home_team,
    away_team,
    home_score,
    away_score
FROM games;

SELECT COUNT(*)
FROM games;



SELECT COUNT(*)
FROM games;


SELECT DISTINCT season, week
FROM games
ORDER BY season, week;

SELECT
    season,
    COUNT(*)
FROM games
WHERE season = 2026
GROUP BY season;

SELECT
    status,
    COUNT(*)
FROM games
WHERE season = 2026
GROUP BY status;

SELECT
    COUNT(*)
FROM games
WHERE season = 2026
AND home_score = 0
AND away_score = 0;

DELETE FROM games
WHERE season = 2026
AND completed = false;

SELECT
    season,
    COUNT(*) as games
FROM games
GROUP BY season
ORDER BY season;

SELECT *
FROM games
WHERE season = 2026
LIMIT 10;