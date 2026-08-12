import redis

def start_redis():
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return redis_client

redis_client = start_redis()
