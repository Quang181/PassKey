
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from . import engine
from src.comman import engine, Session
from sqlalchemy.orm import relationship
Base = declarative_base()


# Định nghĩa bảng `User`
class Account(Base):
    __tablename__ = 'account'

    id = Column(String(100), primary_key=True)
    fullname = Column(String(50))
    email = Column(String(50))
    password = Column(String(100))
    username = Column(String(50))
    #
    # integration_passkeys = relationship("IntegrationPasskey", back_populates="account")

    def get_info_user_by_username(self):
        session = Session()
        info_user = session.query(Account).filter_by(username=self.username).first()
        session.close()

        return info_user

# Tạo bảng trong cơ sở dữ liệu
# Base.metadata.create_all(engine)
# #

# session = Session()
# c = session.query(Account).filter_by(email='email@gmail.com').first()
# print("test")