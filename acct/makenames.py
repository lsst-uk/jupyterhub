import sqlite3

db_file = "jobs.db"

conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute('SELECT * FROM users')
users = c.fetchall()
if users:
    for user in users:
        (uid, name) = user
        print ("%s,,\"%s\"" % (uid, name))
conn.close()

