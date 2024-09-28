from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Chuỗi kết nối đến cơ sở dữ liệu
# Thay đổi 'dialect+driver://username:password@host:port/database' với thông tin thực tế

# DATABASE_URL = "sqlite:///example.db"  # Kết nối SQLite ví dụ
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost/mydatabase"  # Kết nối PostgreSQL
# DATABASE_URL = "mysql+pymysql://user:password@localhost/mydatabase"  # Kết nối MySQL
engine = create_engine('mysql+pymysql://root:1812001q@127.0.0.1:3307/mydb')

# engine = engine.connect()
# print("c")
#
# try:
#     with engine.connect() as connection:
#         print("Kết nối thành công!")
# except Exception as e:
#     print("Lỗi kết nối MySQL:", str(e))

# Tạo Engine
# engine = create_engine(DATABASE_URL)

# Tạo Session để tương tác với cơ sở dữ liệu
# Session = sessionmaker(bind=engine)
# session = Session()