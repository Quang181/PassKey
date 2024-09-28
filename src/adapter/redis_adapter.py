from src.infra.connect_redis import Redis
class RedisAdapter:

    @staticmethod
    def get_connect():
        return Redis()