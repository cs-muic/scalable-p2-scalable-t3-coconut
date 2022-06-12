"""Define functions to use in redis queue."""

import time
import os
import subprocess

from rq import get_current_job

from minio import Minio
from pathlib import Path



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
    time.sleep(20)

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


    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": vdo_input,
        "result": vdo_input,
    }