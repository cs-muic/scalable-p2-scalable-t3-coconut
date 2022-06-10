"""Define functions to use in redis queue."""

import time
import os
import subprocess

from rq import get_current_job

from minio import Minio




def some_long_function(some_input):
    """An example function for redis queue."""
    job = get_current_job()
    # print(job)
    time.sleep(10)

    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }

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
    subprocess.Popen([f'{pwd}/app/extract-frames.sh', f'{pwd}/input_vdo/{video}'])
    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": vdo_input,
        "result": vdo_input,
    }