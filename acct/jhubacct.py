#
# REST service to keep track of active jobs
#

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from math import ceil
import sqlite3
import json
import nacl.encoding
import nacl.signing

app = Flask(__name__)
api = Api(app)

db_file = "jobs.db"
verify_key_hex = ""
verify_key = nacl.signing.VerifyKey(verify_key_hex, encoder=nacl.encoding.HexEncoder)

parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("name")
parser.add_argument("user")
parser.add_argument("group")
parser.add_argument("ctime")
parser.add_argument("start")
parser.add_argument("end")
parser.add_argument("ncpus")
parser.add_argument("mem")
parser.add_argument("status")
parser.add_argument('X-Signature', location='headers')

def validate(data, sig):
    if not sig:
        return False
    try:
        sig = nacl.encoding.URLSafeBase64Encoder.decode(str(sig))
        verify_key.verify(data,sig)
        return True
    #except nacl.exceptions.BadSignatureError:
    except:
        return False

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
        message = request.data
        args = parser.parse_args()
        if not validate(message, args.pop("X-Signature", None)):
            return 'Invalid signature', 400

        if args["id"]:
            return 'Job ID specified in POST request', 405
        if not args["status"]:
            args["status"] = "Q"
        if args["ncpus"]:
            try:
                args["ncpus"] = int(ceil(float(args["ncpus"])))
            except:
                return 'error parsing value for ncpus', 400

        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        for key in args:
            if not args[key]:
                args[key] = ''
        c.execute("INSERT INTO jobs (name,user,'group',ctime,start,end,ncpus,mem,status) VALUES (?,?,?,?,?,?,?,?,?)", 
                (args["name"], args["user"], args["group"], args["ctime"], args["start"], args["end"], args["ncpus"], args["mem"], args["status"]))
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
        message = request.data
        args = parser.parse_args()
        if not validate(message, args.pop("X-Signature", None)):
            return 'Invalid signature', 400

        if args["id"]:
            if int(args["id"]) != int(jobid):
                return 'Mismatched job IDs', 400
            args["id"] = None
        if not args["status"]:
            args["status"] = "Q"
        if args["ncpus"]:
            try:
                args["ncpus"] = int(ceil(float(args["ncpus"])))
            except:
                return 'error parsing value for ncpus', 400

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
            c.execute("INSERT INTO jobs (name,user,'group',ctime,start,end,ncpus,mem,status) VALUES (?,?,?,?,?,?,?,?,?)", 
                    (args["name"], args["user"], args["group"], args["ctime"], args["start"], args["end"], args["ncpus"], args["mem"], args["status"]))
            conn.commit()
            status = 201
        c.execute('SELECT * FROM jobs WHERE id=?', (jobid,))
        job = c.fetchone()
        output = dict((c.description[i][0], value) for i, value in enumerate(job))
        conn.close()
        return output, status

    # create job
    def post(self):
        return '', 501

    # not yet implemented
    def delete(self, jobid):
        return '', 501

class User(Resource):
    # get a user
    def get(self, uid):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE uid=?', (uid,))
        job = c.fetchone()
        fields = c.description
        conn.close()
        if job:
            output = dict((fields[i][0], value) for i, value in enumerate(job))
            return output, 200
        else:
            return "Not found", 404

    # create/update a job
    def put(self, uid):
        message = request.data
        p = reqparse.RequestParser()
        p.add_argument("name")
        p.add_argument('X-Signature', location='headers')
        args = p.parse_args()
        if not validate(message, args.pop("X-Signature", None)):
            return 'Invalid signature', 400

        if not args["name"]:
            args["name"] = ""

        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE uid=?", (uid,))
        job = c.fetchone()
        if job:
            # do update
            c.execute('UPDATE users SET name=? WHERE uid=?', (args["name"], uid))
            conn.commit()
            status = 200
        else:
            # do create
            c.execute("INSERT INTO users (uid,name) VALUES (?,?)",
                    (uid, args["name"]))
            conn.commit()
            status = 201
        c.execute('SELECT * FROM users WHERE uid=?', (uid,))
        user = c.fetchone()
        output = dict((c.description[i][0], value) for i, value in enumerate(user))
        conn.close()
        return output, status


api.add_resource(JobList, "/job")
api.add_resource(Job, "/job/<string:jobid>")
api.add_resource(User, "/user/<string:uid>")

if (__name__ == '__main__'):
    app.run(debug=True, port=5000)

