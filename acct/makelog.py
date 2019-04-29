import sqlite3
from datetime import datetime

db_file = "jobs.db"
hostname = "jhub"

conn = sqlite3.connect(db_file)
c = conn.cursor()
c.execute('SELECT * FROM jobs WHERE status="E"')
jobs = c.fetchall()
if jobs:
    for job in jobs:
        (jobid, name, user, ctime, start, end, ncpus, mem, status) = job
        print ("%s;E;%d; user=%s jobname=%s ctime=%d start=%s end=%d exec_host=%s/0*%d Resource_List.ncpus=%d Resource_List.mem=%s" % (
            datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
            jobid,
            user,
            name,
            ctime,
            start,
            end,
            hostname,
            ncpus,
            ncpus,
            mem
            ))
        c.execute('UPDATE jobs SET status="X" WHERE id=?', (jobid, ))
conn.commit()
conn.close()

