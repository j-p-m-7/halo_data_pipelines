SELECT 
    conname AS constraint_name, 
    contype AS constraint_type 
FROM 
    pg_constraint 
WHERE 
    conrelid = (
        SELECT oid 
        FROM pg_class 
        WHERE relname = 'matches'
    );