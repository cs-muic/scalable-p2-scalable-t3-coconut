"""Define functions to use in redis queue."""

import time
import os
import subprocess

from rq import get_current_job

from minio import Minio
from pathlib import Path
from rq.job import Job
from .redis_resc import redis_queue_com

job_com = Job


def execute_extract(vdo_input):
    job = get_current_job()
    pwd = os.getcwd()
    video = vdo_input.get('video')
    client = Minio(
        "127.0.0.1:7000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )
    client.fget_object("video", str(video), f'{pwd}/input_vdo/{video}')
    work = subprocess.Popen([f'{pwd}/app/extract-frames.sh', f'{pwd}/input_vdo/{video}'])
    # time.sleep(20)
    work.wait()

    directory = f'{pwd}/frames'
    # file = "frame-001.png"

    # client.fput_object("frames", str(file), f'{directory}/{file}')
 
    # iterate over files in
    # that directory
    files = Path(directory).glob('*')
    num = 1
    for file in files:
        # print(file)
        client.fput_object("frames", f"frame-{num}.png", str(file))
        num += 1

    job_com = redis_queue_com.enqueue(execute_compose, vdo_input)
    


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

    client = Minio(
        "127.0.0.1:7000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    for item in client.list_objects("frames",recursive=True):
        client.fget_object("frames",item.object_name,f'{pwd}/incoming-frames/{item.object_name}')

    work = subprocess.Popen([f'{pwd}/app/gif-composer.sh', f'{pwd}/output-gif/{gif}'])
    work.wait()


    client.fput_object("gif", gif, f'{pwd}/output-gif/{gif}')





    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": gif_input,
        "result": gif_input,
    }


# def log_stream(job_ex: Job, job_com: Job):
#     # log = {job_ex.id: "extracting"}
#     if (job_ex.get_status() == "finished") and (job_com.get_status != "failed"):
#         # log.values = "composing"
#         return {job_ex.id: "composing"}
#     elif (job_ex.get_status() == "finished") and (job_com.get_status == "finished"):
#         return {job_ex.id: "finished"}
#     elif (job_ex.get_status() == "failed") or (job_com.get_status == "failed"):
#         return {job_ex.id: "failed"}
#     return {job_ex.id: "extracting"}

def log_stream(input_id):
    # log = {job_ex.id: "extracting"}
    job_ex_status = input_id.get("job_ex")
    job_com_status = input_id.get("job_com")
    if (job_ex_status == "finished") and (job_com_status != "failed"):
        # log.values = "composing"
        return "composing"
    elif (job_ex_status == "finished") and (job_com_status == "finished"):
        return "finished"
    elif (job_ex_status == "failed") or (job_com_status == "failed"):
        return "failed"
    return "extracting"