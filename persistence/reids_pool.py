import redis

from settings import REDIS_POOL_SIZE, REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

redis_config = {
    "max_connections": REDIS_POOL_SIZE,  # 最大连接数比最大可工作线程数多1
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": REDIS_DB,
    "password": REDIS_PASSWORD,
    "decode_responses": True,
}

redis_pool = redis.ConnectionPool(**redis_config)
