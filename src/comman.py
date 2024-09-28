from sqlalchemy.orm import declarative_base, sessionmaker
SECRET_KEY = "quang181"
rp_id = "localhost"
rp_name = "Vcc"
# Connet mysql
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:1812001q@127.0.0.1:3307/mydb')

Session = sessionmaker(bind=engine)


