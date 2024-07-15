SELECT DISTINCT
	playlist_map_mode_pair__asset_id AS "asset_id",
	playlist_map_mode_pair__version_id AS "version_id"
FROM 
	GRUNT_CLEANING.MATCHES
WHERE
	playlist_map_mode_pair__asset_id IS NOT NULL
	AND playlist_map_mode_pair__version_id IS NOT NULL
;