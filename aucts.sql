-- CREATE TABLE IF NOT EXISTS auctions(
		auction_id serial PRIMARY KEY,
		date TIMESTAMP NOT NULL,
		square VARCHAR(600) NOT NULL,
		area VARCHAR(600) NOT NULL,
		status VARCHAR(30) NOT NULL,
		submit_deadline VARCHAR(100),
		contribution INTEGER NOT NULL,
		organizer VARCHAR(100) NOT NULL
);