SELECT DATE(match_info__start_time) 
FROM grunt.MATCHES 
ORDER BY match_info__start_time DESC
LIMIT 1;