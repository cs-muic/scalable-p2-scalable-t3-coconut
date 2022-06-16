"""The Flask App."""

# pylint: disable=broad-except

from crypt import methods
import json
import subprocess
from time import sleep
from flask import Flask, abort, jsonify, request
from rq.job import Job
from minio import Minio
from pathlib import Path
import os
from flask_cors import CORS
import shutil
import base64 

from .functions import execute_extract, log_stream
from .redis_resc import redis_conn, redis_queue_ex

app = Flask(__name__)
CORS(app)

job_ex = Job

client = Minio(
    "0.0.0.0:7000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)


@app.errorhandler(404)
def resource_not_found(exception):
    """Returns exceptions as part of a json."""
    return jsonify(error=str(exception)), 404


@app.route("/api/")
def home():
    """Show the app is working."""
    return "Running!"


@app.route("/api/enqueue", methods=["POST", "GET"])
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
    #= submited video
    # job_con = redis_queue_com.enqueue(execute_compose, data)    
    # job_ex, job_com

    return jsonify({"job_id": job_ex.id})



@app.route("/api/check_status")
def check_status():
    """Takes a job_id and checks its status in redis queue."""
    job_id = request.args["job_id"]

    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception as exception:
        abort(404, description=exception)

    return jsonify({"job_id": job.id, "job_status": job.get_status()})


@app.route("/api/get_status")
def get_status():
    # job_com = Job.fetch(job_com.id, connection=redis_conn)
    # {job_id_ex: status}
    # video_name = current_data.get('video')
    # data = jsonify({"job_ex":job_ex.get_status(), "job_com":job_com.get_status()})
    # job = redis_queue_log.enqueue(log_stream)
    log_job_id = redis_conn.get('log_job_id')
    job = Job.fetch(str(log_job_id).split("'")[1], connection=redis_conn)
    return job.result


@app.route("/api/enqueue_bucket", methods=["POST"])
def enqueue_bucket():
    if request.method == "POST":
        data = request.json

    bucket_name = data.get('bucket')

    pwd = os.getcwd()
    
    for item in client.list_objects(bucket_name,recursive=True):
        client.fget_object(bucket_name,item.object_name,f'{pwd}/input-vdo/{item.object_name}')
    
    directory = f'{pwd}/input-vdo'

    all_jobs = {}

    files = Path(directory).glob('*')
    for file in files:
        video = str(file).split("/")[-1]
        data = {
            "video" : video, 
            "gif": video.split(".")[0] + ".gif"
        }
        job = redis_queue_ex.enqueue(execute_extract, data)
        all_jobs[video] = job.get_status()

    return jsonify(all_jobs)


@app.route("/api/get_result")
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


@app.route("/api/all_gif", methods=["POST"])
def get_all_gif():
    
    if request.method == "POST":
        data = request.json

    bucket_name = data.get('bucket')
    all_gif = []
    pwd = os.getcwd()


    for item in client.list_objects(bucket_name,recursive=True):
        if item.object_name.endswith(".gif") :
            all_gif.append({"gif": item.object_name})

            image = open(f"{pwd}/output-gif/{item.object_name}", 'rb') #open binary file in read mode
            image_read = image.read()
            image_64_encode = base64.b64encode(image_read)

            filename = item.object_name.split(".gif")[0]
            subprocess.Popen(['echo', f'{image_64_encode}', '>', f'{pwd}/base64-gif/{filename}.txt'])
            # shutil.copy2(f"{pwd}/output-gif/{filename}.txt", f"{pwd}/base64-gif/{filename}.txt")


    return jsonify({"gifs": all_gif})


@app.route("/api/all_video")
def get_all_video():
    all_video = []

    # count = 1

    for item in client.list_objects("video",recursive=True):
        if item.object_name.endswith(".mp4") :
            all_video.append({"vdo":item.object_name})
            # all_video[f"{count}"] = f"{item.object_name}"
            # count +=1

    return jsonify({"vids": all_video})


@app.route("/api/delete_all_gif")
def delete_all_gif():
    pwd = os.getcwd()
    for item in client.list_objects("gif",recursive=True):
        if item.object_name.endswith(".gif") :
            client.remove_object("gif", item.object_name)
            os.remove( f'{pwd}/output-gif/{item.object_name}')

    return jsonify({})

@app.route("/api/delete_gif", methods=["POST"])
def delete_gif():
    if request.method == "POST":
        data = request.json

    gif_name = data.get('gif')
    client.remove_object("gif", gif_name)
    pwd = os.getcwd()
    os.remove( f'{pwd}/output-gif/{gif_name}')
    return jsonify({})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000 ,debug=True)