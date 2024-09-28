import redis
from pydantic.v1 import NoneStr

# Tạo kết nối tới Redis server
r = redis.Redis(
    host='localhost',  # Địa chỉ server Redis (thường là localhost nếu chạy trên máy)
    port=6379,         # Cổng mặc định của Redis
      # Nếu Redis có yêu cầu password, điền vào đây. Nếu không, để trống.
         # Chọn database (0 là database mặc định)
)

class Redis:
    localhost = "localhost"
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

    def set_value(self,key, value, expire=None) -> None:
        if expire is None:
            self.redis_cli.set(key, value)
        else:
            self.redis_cli.set(key, value, ex=expire)

    def delete_key(self, key):

        self.redis_cli.delete(key)

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