SELECT DISTINCT PLAYER_ID, replace(replace(PLAYER_ID, 'xuid(', ''), ')', '') AS xuid_numeric, '' AS gamertag
FROM SPARTAN.MATCH_DET_PLAYERS
WHERE LENGTH(PLAYER_ID) > 9;