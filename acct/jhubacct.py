from flask import Flask
from flask_restful import Api, Resource, reqparse
from math import ceil
import sqlite3
import json

app = Flask(__name__)
api = Api(app)

db_file = "jobs.db"

class JobList(Resource):
    # get a list of jobs
    def get(self):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM jobs')
        jobs = c.fetchall()
        fields = c.description
        conn.close()
        output = []
        if jobs:
            for job in jobs:
                output.append(dict((fields[i][0], value) for i, value in enumerate(job)))
        return output, 200

    # create a job
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("user")
        parser.add_argument("ctime")
        parser.add_argument("start")
        parser.add_argument("end")
        parser.add_argument("ncpus")
        parser.add_argument("mem")
        parser.add_argument("status")
        args = parser.parse_args()

        if args["id"]:
            return 'Job ID specified in POST request', 405
        if not args["status"]:
            args["status"] = "Q"

        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        for key in args:
            if not args[key]:
                args[key] = ''
        c.execute("INSERT INTO jobs (name,user,ctime,start,end,ncpus,mem,status) VALUES (?,?,?,?,?,?,?,?)", 
                (args["name"], args["user"], args["ctime"], args["start"], args["end"], int(ceil(args["ncpus"])), args["mem"], args["status"]))
        jobid = c.lastrowid
        conn.commit()
        status = 201
        c.execute('SELECT * FROM jobs WHERE id=?', (jobid,))
        job = c.fetchone()
        output = dict((c.description[i][0], value) for i, value in enumerate(job))
        conn.close()
        return output, status


class Job(Resource):
    # get a job
    def get(self, jobid):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM jobs WHERE id=?', (jobid,))
        job = c.fetchone()
        fields = c.description
        conn.close()
        if job:
            output = dict((fields[i][0], value) for i, value in enumerate(job))
            return output, 200
        else:
            return "Not found", 404

    # create/update a job
    def put(self, jobid):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("name")
        parser.add_argument("user")
        parser.add_argument("ctime")
        parser.add_argument("start")
        parser.add_argument("end")
        parser.add_argument("ncpus")
        parser.add_argument("mem")
        parser.add_argument("status")
        args = parser.parse_args()

        if args["id"]:
            if int(args["id"]) != int(jobid):
                return 'Mismatched job IDs', 400
            args["id"] = None
        if not args["status"]:
            args["status"] = "Q"

        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM jobs WHERE id=?", (jobid,))
        job = c.fetchone()
        if job:
            # do update
            for key in args:
                if args[key]:
                    c.execute('UPDATE jobs SET '+key+'=? WHERE id=?', (args[key], jobid))
            conn.commit()
            status = 200
        else:
            # do create
            for key in args:
                if not args[key]:
                    args[key] = ''
            c.execute("INSERT INTO jobs (name,user,ctime,start,end,ncpus,mem,status) VALUES (?,?,?,?,?,?,?,?)", 
                    (args["name"], args["user"], args["ctime"], args["start"], args["end"], int(ceil(args["ncpus"])), args["mem"], args["status"]))
            conn.commit()
            status = 201
        c.execute('SELECT * FROM jobs WHERE id=?', (jobid,))
        job = c.fetchone()
        output = dict((c.description[i][0], value) for i, value in enumerate(job))
        conn.close()
        return output, status

    # create job
    def post(self):
        return 'create', 200

    # not yet implemented
    def delete(self, jobid):
        return '', 501

api.add_resource(JobList, "/job")
api.add_resource(Job, "/job/<string:jobid>")

if (__name__ == '__main__'):
    app.run(debug=True)

