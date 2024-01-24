import os
import redis
from django.conf import settings
from urllib.parse import urlparse


def redis_instance():
    # connect to redis
    
    print("redis ",settings.REDIS_URL)
    if settings.REDIS_SSL:
        url = urlparse(settings.REDIS_URL)
        ri = redis.Redis(
            host=url.hostname,
            port=url.port,
            password=url.password,
            ssl=True,
            ssl_cert_reqs=None,
        )
        print(" data1 " )
    else:
        ri = redis.Redis.from_url(settings.REDIS_URL, db=0)
        print(" data2 " )
    print(" data " ,ri)
    return ri
