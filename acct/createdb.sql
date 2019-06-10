CREATE TABLE jobs (
	id INTEGER PRIMARY KEY,
	name TEXT, 
	user TEXT, 
	group TEXT, 
	ctime INTEGER, 
	start INTEGER, 
	end INTEGER, 
	ncpus INTEGER, 
	mem TEXT, 
	status TEXT
);

CREATE TABLE users (
        uid TEXT,
        name TEXT
);

