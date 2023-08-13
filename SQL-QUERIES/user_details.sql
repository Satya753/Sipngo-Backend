
CREATE TABLE user_details(
	user_id VARCHAR(64),
	user_name VARCHAR(64),
	user_email VARCHAR(64),
	user_password VARCHAR(64),
	user_location VARCHAR(64)
)	

ALTER TABLE user_details ADD PRIMARY KEY (user_id);
