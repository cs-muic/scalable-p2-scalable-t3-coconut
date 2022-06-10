# """Define functions to use in redis queue."""

import time
import os
import subprocess

from rq import get_current_job


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
    subprocess.Popen([f'{pwd}/app/gif-composer.sh', f'{pwd}/app/{gif}'])
    return {
        "job_id": job.id,
        "job_enqueued_at": job.enqueued_at.isoformat(),
        "job_started_at": job.started_at.isoformat(),
        "input": input,
        "result": input,
    }