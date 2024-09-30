import redis
from pydantic.v1 import NoneStr


# Tạo kết nối tới Redis server
# r = redis.Redis(
#     host='123.30.48.240',  # Địa chỉ server Redis (thường là localhost nếu chạy trên máy)
#     port=6379,         # Cổng mặc định của Redis
#       # Nếu Redis có yêu cầu password, điền vào đây. Nếu không, để trống.
#          # Chọn database (0 là database mặc định)
# )
#
# c = r.rpush("test", *["|1,", "b", "c"])
#
# u = r.lrange("test", 0, -1)
# print("cc")
class Redis:
    localhost = "123.30.48.240"
    port = 6379

    def __init__(self):
        self.redis_cli = self.connect_redis()

    def connect_redis(self):
        connect = redis.Redis(
            host=self.localhost,  # Địa chỉ server Redis (thường là localhost nếu chạy trên máy)
            port=self.port,  # Cổng mặc định của Redis
            # Nếu Redis có yêu cầu password, điền vào đây. Nếu không, để trống.
            # Chọn database (0 là database mặc định)
        )
        return connect

    def get_value_by_key(self, key):
        value = self.redis_cli.get(key)
        return value

    def set_value(self, key, value, expire=None) -> None:
        if expire is None:
            self.redis_cli.set(key, value)
        else:
            self.redis_cli.set(key, value, ex=expire)

    def delete_key(self, key):

        self.redis_cli.delete(key)

    ####

    async def set_data_list(self, key, data: list, expire=None) -> None:
        save_data = self.redis_cli.rpush(key, *data)
        if expire:
            set_expire = self.redis_cli.expire(key, expire)


    async def list_value(self, key, start=0, stop=-1):
        return self.redis_cli.lrange(key, start, stop)
# # Đặt một giá trị (set key-value)
# r.set('name', 'John Doe')
#
# # Lấy giá trị theo key
# name = r.get('name')
# print(f"Name: {name.decode('utf-8')}")

if __name__ == '__main__':
    print("c")

    c = r.get("name")

    print("s+++++++++++++++++++++++++++")
