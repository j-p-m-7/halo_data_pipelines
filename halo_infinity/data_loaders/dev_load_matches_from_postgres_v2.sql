SELECT MATCH_ID
FROM GRUNT_STAGING.MATCHES
WHERE MATCH_ID NOT IN (SELECT MATCH_ID FROM GRUNT_STAGING.MATCH_DET)
ORDER BY MATCH_INFO__START_TIME ASC;