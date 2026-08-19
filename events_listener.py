from app.redis import redis_client


#from redis.redis_client import redis_client
def revisarFechaExpirada():
    sub = redis_client.redis_client.pubsub()
    sub.subscribe("__keyevent@0__:expired")

    for mensaje in sub.listen():
        if mensaje["type"] == "message":
            print(mensaje["data"])

revisarFechaExpirada()