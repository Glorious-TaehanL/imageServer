import redis
import os

def redis_connection():
    rd = redis.StrictRedis(
        host=os.environ[''], 
        port=6379, 
        db=0
        )

    return rd