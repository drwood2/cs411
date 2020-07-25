-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS req;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE req (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  req_date TEXT NOT NULL,
  req_time TEXT NOT NULL,
  location TEXT NOT NULL,
  priority INTEGER NOT NULL,
  capacity INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id)
);
