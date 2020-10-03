import sqlite3

conn = sqlite3.connect('ximalaya.db')

c = conn.cursor()

c.execute('''CREATE TABLE "track" (
	"id"	INTEGER,
	"albumId"	TEXT NOT NULL,
	"trackId"	TEXT NOT NULL,
	"trackIndex"	INTEGER NOT NULL DEFAULT 0,
	"title"	TEXT NOT NULL,
	"url"	TEXT,
	"done"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("albumId","trackIndex"),
	UNIQUE("albumId","trackId")
);''')

conn.commit()

print("init ximalaya.db done")
