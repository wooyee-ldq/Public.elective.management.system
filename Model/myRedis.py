# coding:utf-8


import redis


class MyRedis(object):

    pool = redis.ConnectionPool(host="127.0.0.1", port=6379, decode_responses=True)

    @classmethod
    def get_redis(cls):
        return redis.Redis(connection_pool=cls.pool)
