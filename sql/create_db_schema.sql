DROP TABLE IF EXISTS current_voting_periods;
DROP TABLE IF EXISTS voting_period_history;


--- BINGO TASKS

CREATE TABLE tasks (
	task_id SERIAL NOT NULL,
    point_value INT NOT NULL,
    task_name VARCHAR(500) NOT NULL,
    PRIMARY KEY (task_id)
);