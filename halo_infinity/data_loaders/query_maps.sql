SELECT DISTINCT
	map_variant__asset_id AS "asset_id",
	map_variant__version_id AS "version_id"
FROM 
	GRUNT_CLEANING.MATCHES
WHERE
	map_variant__asset_id IS NOT NULL
	AND map_variant__version_id IS NOT NULL
;