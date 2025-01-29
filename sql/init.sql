USE crosswords;

CREATE TABLE words (
	hash_id VARCHAR(100) PRIMARY KEY NOT NULL, 
    language VARCHAR(10) NOT NULL,
    word VARCHAR(255) NOT NULL,
    theme VARCHAR(100) NOT NULL
)