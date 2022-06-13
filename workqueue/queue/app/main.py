"""The Flask App."""

# pylint: disable=broad-except

import json
from time import sleep
from flask import Flask, abort, jsonify, request
from rq.job import Job

from .functions import execute_extract, log_stream, job_com
from .redis_resc import redis_conn, redis_queue_ex, redis_queue_log

app = Flask(__name__)

job_ex = Job


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


@app.route("/")
def home():
    """Show the app is working."""
    return "Running!"


@app.route("/enqueue", methods=["POST", "GET"])
def enqueue():
    """Enqueues a task into redis queue to be processes.
    Returns the job_id."""
    if request.method == "GET":
        query_param = request.args.get("external_id")
        if not query_param:
            abort(
                404,
                description=(
                    "No query parameter external_id passed. "
                    "Send a value to the external_id query parameter."
                ),
            )
        data = {"external_id": query_param}
    if request.method == "POST":
        data = request.json

    job_ex = redis_queue_ex.enqueue(execute_extract, data)


    # job_con = redis_queue_com.enqueue(execute_compose, data)
        
    
    return jsonify({"job_id": job_ex.id})



@app.route("/check_status")
def check_status():
    """Takes a job_id and checks its status in redis queue."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        abort(404, description=exception)

    return jsonify({"job_id": job.id, "job_status": job.get_status()})


@app.route("/get_status")
def get_status():
    # job_ex = Job.fetch(job_ex.id, connection=redis_conn)
    # job_com = Job.fetch(job_com.id, connection=redis_conn)
    job = redis_queue_log.enqueue(log_stream, {"job_ex":job_ex.get_status, "job_com":job_com.get_status})
    return jsonify({"job_status": job.result})


@app.route("/enqueue_bucket")
def enqueue_bucket():
    bucket = request.args["bucket"]
    if request.method == "GET":
        query_param = request.args.get("external_id")
        if not query_param:
            abort(
                404,
                description=(
                    "No query parameter external_id passed. "
                    "Send a value to the external_id query parameter."
                ),
            )
        data = {"external_id": query_param}
    if request.method == "POST":
        data = request.json

    job_ex = redis_queue_ex.enqueue(execute_extract, data)




@app.route("/get_result")
def get_result():
    """Takes a job_id and returns the job's result."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        abort(404, description=exception)

    if not job.result:
        abort(
            404,
            description=f"No result found for job_id {job.id}. Try checking the job's status.",
        )
    return jsonify(job.result)






if __name__ == "__main__":
    app.run(debug=True)