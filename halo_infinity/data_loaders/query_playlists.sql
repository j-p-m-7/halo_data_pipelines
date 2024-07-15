SELECT DISTINCT
	playlist__asset_id AS "asset_id",
	playlist__version_id AS "version_id"
FROM 
	GRUNT_CLEANING.MATCHES
WHERE
	-- playlist__asset_id IS NOT NULL
	AND playlist__version_id IS NOT NULL
;