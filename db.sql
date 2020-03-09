PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "todo_t" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT NOT NULL,
	"detail"	TEXT
);
INSERT INTO todo_t VALUES(1,'book','todo for textbook');
INSERT INTO todo_t VALUES(2,'keep','keep something in a timeline');
CREATE TABLE IF NOT EXISTS "todo_book" (
	"id"	INTEGER,
	"start"	INTEGER NOT NULL,
	"end"	INTEGER NOT NULL,
	"val"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "todo_keep" (
	"id"	INTEGER,
	"span"	INTEGER NOT NULL,
	"open"	INTEGER NOT NULL,
	"close"	INTEGER NOT NULL,
	"repeat"	INTEGER NOT NULL DEFAULT 1,
	"val"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "credit" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"uid"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"is_spent"	INTEGER NOT NULL DEFAULT 0,
	"is_loop"	INTEGER DEFAULT 0,
	"price"	REAL NOT NULL,
	"dependency"	INTEGER DEFAULT -1,
	"timestamp"	TEXT,
	"trash"	INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "pow" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"uid"	INTEGER NOT NULL,
	"todoid"	INTEGER NOT NULL,
	"note"	TEXT NOT NULL,
	"proof"	TEXT,
	"timestamp"	TEXT,
	"is_public"	INTEGER DEFAULT 0,
	"trash"	INTEGER DEFAULT 0,
	FOREIGN KEY("todoid") REFERENCES "todo"("id")
);

CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT UNIQUE,
	"passwd"	TEXT,
	"motto"	TEXT DEFAULT '5ZCD57KR57KR',
	"hold"	REAL DEFAULT 0,
	"visible"	INTEGER DEFAULT 0,
	"share"	TEXT
);

CREATE TABLE IF NOT EXISTS "todo" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"uid"	INTEGER NOT NULL,
	"iid"	INTEGER NOT NULL,
	"tid"	INTEGER NOT NULL,
	"name"	INTEGER NOT NULL,
	"rate"	REAL NOT NULL DEFAULT 1,
	"dependency"	INTEGER DEFAULT -1,
	"is_finished"	INTEGER DEFAULT 0,
	"trash"	INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS "user_bond" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"uid"	INTEGER NOT NULL,
	"iid"	INTEGER NOT NULL,
	"pipe"	INTEGER
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('todo_t',0);
INSERT INTO sqlite_sequence VALUES('credit',0);
INSERT INTO sqlite_sequence VALUES('pow',0);
INSERT INTO sqlite_sequence VALUES('user',0);
INSERT INTO sqlite_sequence VALUES('todo',0);
COMMIT;
