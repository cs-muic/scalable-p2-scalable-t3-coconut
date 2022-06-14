"""Define functions to use in redis queue."""

from cmath import log
import json
from multiprocessing import connection
import time
import os
import subprocess

from rq import get_current_job

from minio import Minio
from pathlib import Path
from rq.job import Job
from .redis_resc import redis_queue_com, redis_queue_log, redis_conn

from .main import current_job_id

client = Minio(
    "127.0.0.1:7000",
    access_key="minio",
    secret_key="minio123",
    secure=False
)

def execute_extract(vdo_input):

    job = get_current_job()
    log_data = {
        "id": current_job_id,
        "vdo_name": vdo_input.get('video'),
        "status": "submitted"
        }
    redis_queue_log.enqueue(log_stream, log_data)

    pwd = os.getcwd()
    video = vdo_input.get('video')

    client.fget_object("video", str(video), f'{pwd}/input-vdo/{video}')
    work = subprocess.Popen([f'{pwd}/app/extract-frames.sh', f'{pwd}/input-vdo/{video}'])
    
    work.wait()

    directory = f'{pwd}/frames'

    files = Path(directory).glob('*')
    num = 1
    dir_name = str(video).split(".")[0]
    for file in files:
        # print(file)
        client.fput_object("frames", f"{dir_name}/frame-{num}.png", str(file))
        num += 1

    if job.get_status() == "failed":
        log_data = {
            "id": current_job_id, 
            "vdo_name": vdo_input.get('video'),
            "status": "failed"
            }
        redis_queue_log.enqueue(log_stream, log_data)
    else:
        log_data = {
            "id": current_job_id,
            "vdo_name": vdo_input.get('video'),
            "status": "extracted"
            }
        redis_queue_log.enqueue(log_stream, log_data)

    redis_queue_com.enqueue(execute_compose, vdo_input)
    # redis_queue_log.enqueue() = 
    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": vdo_input,
        "result": vdo_input,
    }


def execute_compose(gif_input):
    job = get_current_job()
    pwd = os.getcwd()
    gif = gif_input.get('gif')

    dir_name = str(gif).split(".")[0]
    for item in client.list_objects("frames",recursive=True):
        client.fget_object("frames",item.object_name,f'{pwd}/incoming-frames/{item.object_name}')
        # subprocess.Popen(['echo', f"{item.object_name}"])

    work = subprocess.Popen([f'{pwd}/app/gif-composer.sh', dir_name, f'{pwd}/output-gif/{gif}'])
    work.wait()

    client.fput_object("gif", gif, f'{pwd}/output-gif/{gif}')
    # redis_queue_log.enqueue() = composed
    
    
    if job.get_status() == "failed":
        log_data = {
            "id": current_job_id, 
            "vdo_name": gif_input.get('video'),
            "status": "failed"
            }
        redis_queue_log.enqueue(log_stream, log_data)
    else:
        log_data = {
            "id": current_job_id, 
            "vdo_name": gif_input.get('video'),
            "status": "composed"
            }
        redis_queue_log.enqueue(log_stream, log_data)
    
    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": gif_input,
        "result": gif_input,
    }


def log_stream(log_data):
    return {
        "job_id" : log_data.get('id'),
        "vid_name": log_data.get('vdo_name'),
        "job_status": log_data.get('status')
        }

