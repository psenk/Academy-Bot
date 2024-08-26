DROP TABLE IF EXISTS active_voting_periods;
DROP TABLE IF EXISTS past_voting_periods;

CREATE TABLE active_voting_periods (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    nominee VARCHAR(100),
    comments VARCHAR(1000),
    member_ids BIGINT[] NOT NULL,
	voted_ids BIGINT[],
    votes JSONB[],
	start_date TIMESTAMP NOT NULL,
	length INT NOT NULL
);

CREATE TABLE past_voting_periods (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    nominee VARCHAR(100),
    comments VARCHAR(1000),
    member_ids BIGINT[] NOT NULL,
	voted_ids BIGINT[],
    votes JSONB NOT NULL,
	start_date TIMESTAMP NOT NULL,
	length INT NOT NULL
);