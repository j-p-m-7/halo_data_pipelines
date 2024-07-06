SELECT DATE(match_info__start_time) 
FROM spartan.MATCHES 
ORDER BY match_info__start_time DESC
LIMIT 1;