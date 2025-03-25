import os

import redis

PRINTER_ONLINE_KEY = "printer_online"

redis = redis.StrictRedis(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT"),
    decode_responses=True,
)
