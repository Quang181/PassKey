from sqlalchemy.orm import declarative_base, sessionmaker
SECRET_KEY = "quang181"
rp_id = "123.30.48.240"
rp_name = "Vcc"
# Connet mysql
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:1812001q@123.30.48.240:3307/mydb')

Session = sessionmaker(bind=engine)


