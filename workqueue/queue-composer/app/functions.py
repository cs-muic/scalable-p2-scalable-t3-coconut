# """Define functions to use in redis queue."""

import time
import os
import subprocess

from rq import get_current_job

from minio import Minio
from pathlib import Path


def some_long_function(some_input):
    # """An example function for redis queue."""
    job = get_current_job()
    time.sleep(1)
    # print("working")

    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": some_input,
        "result": some_input,
    }

def execute_compose(input):
    job = get_current_job()
    pwd = os.getcwd()
    gif = input.get('gif')

    client = Minio(
        "127.0.0.1:7000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    for item in client.list_objects("frames",recursive=True):
        client.fget_object("frames",item.object_name,f'{pwd}/incoming-frames/{item.object_name}')

    subprocess.Popen([f'{pwd}/app/gif-composer.sh', f'{pwd}/output-gif/{gif}'])

    time.sleep(10)

    client.fput_object("gif", gif, f'{pwd}/output-gif/{gif}')



    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": input,
        "result": input,
    }
