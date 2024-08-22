DROP TABLE IF EXISTS current_votes;
DROP TABLE IF EXISTS past_votes;

CREATE TABLE current_votes (
    id SERIAL PRIMARY KEY,
    nominee VARCHAR(100),
    members VARCHAR(100)[] NOT NULL,
    votes JSONB NOT NULL
);


CREATE TABLE past_votes (
    id SERIAL PRIMARY KEY,
    nominee VARCHAR(100),
    members VARCHAR(100)[] NOT NULL,
    votes JSONB NOT NULL
);