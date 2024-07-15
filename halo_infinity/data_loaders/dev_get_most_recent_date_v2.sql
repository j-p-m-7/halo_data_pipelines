SELECT DATE(match_info__start_time) 
FROM grunt_staging.MATCHES 
ORDER BY match_info__start_time DESC
LIMIT 1;