"""Sets up the redis connection and the redis queue."""
import os

import redis
from rq import Queue

redis_conn = redis.Redis(
    host=os.getenv("REDIS_HOST", "127.0.0.1"),
    port=os.getenv("REDIS_PORT", "6379"),
    password=os.getenv("REDIS_PASSWORD", ""),
)
redis_conn.mset({"latest_job_id": 1})

redis_queue_ex = Queue("extract",connection=redis_conn)
redis_queue_com = Queue("compose",connection=redis_conn)
redis_queue_log = Queue("log",connection=redis_conn)
# redis_queue_com.empty()