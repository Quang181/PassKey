from requests import session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
# from . import engine
from src.comman import engine, Session
Base = declarative_base()

class IntegrationPasskey(Base):
    __tablename__ = 'integration_passkey'

    id = Column(String(100), primary_key=True)
    account_id = Column(String(100), ForeignKey('accounts.id'))
    credential_id = Column(String(100))
    credential_public_key = Column(String(100))
    sign_count = Column(Integer, default=0)
    aaguid = Column(String(100)) # Mã định danh của sản phẩm dùng để xác thực
    fmt = Column(String(20))  # Cho phép NULL
    __table_args__ = (
        CheckConstraint("fmt IN (fido-u2f, packed, tpm, apple, android-safetynet, android-key) OR fmt IS NULL', name='check_fmt_column"),
    )
    credential_type = Column(String(30), default="public_key")
    # user_verified =
    # attestation_object
    credential_device_type = Column(String(30), Enum("platform", "cross-platform")) # platform là vân tay, nhận diện khuôn mặt ... cross-platform là USB ...
    # credential_backed_up
    status = Column(String, Enum("active", "inactive", "delete"))
    create_on = Column(DateTime)
    update_one = Column(DateTime)


    async def get_integration_by_user(self):
        session = Session()
        info_integration = session.query(IntegrationPasskey).filter_by(account_id=self.account_id, status="active").first()
        session.close()

        return info_integration


    async def create_integration(self):
        try:
            session = Session()

            info_integration = IntegrationPasskey(id=self.id, account_id=self.account_id,
                                                  credential_id=self.credential_id,
                                                  credential_public_key=self.credential_public_key,
                                                  sign_count=self.sign_count, aaguid=self.aaguid,
                                                  fmt=self.fmt, create_on=self.create_on, update_one=self.update_one)
            session.add(info_integration)
            session.close()

            status_create = True
        except:
            status_create = False

        return status_create

    async def check_credential(self):
        session = Session()
        info_credential = session.query(IntegrationPasskey).filter(IntegrationPasskey.credential_id == self.credential_id,
                                                        IntegrationPasskey.status != self.status).first()
        session.close()

        return info_credential