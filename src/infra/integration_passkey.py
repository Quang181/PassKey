from OpenSSL.rand import status
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint, Enum, LargeBinary, BINARY, update
from sqlalchemy.ext.declarative import declarative_base
# from . import engine
from src.comman import engine, Session
from sqlalchemy.orm import relationship

Base = declarative_base()

class IntegrationPasskey(Base):
    __tablename__ = 'integration_passkey'

    id = Column(String(100), primary_key=True)
    cre_id = Column(String(100))
    account_id = Column(String(100))
    sign_count = Column(Integer)
    aaguid = Column(String(1024))
    public_key_alg = Column(String(100))  # Mã định danh của sản phẩm dùng để xác thực
    public_key = Column(String(200))  # Cho phép NULL
    status = Column(String(20), Enum("active", "inactive", "delete"))
    create_on = Column(DateTime)
    update_one = Column(DateTime)
    #
    # account = relationship("Account", back_populates="integration_passkeys")

    async def get_integration_by_user(self):
        session = Session()
        info_integration = session.query(IntegrationPasskey).filter_by(account_id=self.account_id,
                                                                       status="active").all()
        session.close()

        return info_integration

    async def create_integration(self):
        try:
            session = Session()

            # return {
            #     "id": cls.gen_id_account(),
            #     "account_id": info_account.get("account_id"),
            #     "sign_count": data_verify.sign_count,
            #     "aaguid": data_verify.attested_data.aaguid,
            #     "attestation": data_verify.attestation,
            #     "public_key_alg": data_verify.public_key_alg,
            #     "public_key": data_verify.public_key,
            #     "create_on": cls.get_time_now(),
            #     "update_one": cls.get_time_now(),
            #     "status": "active"
            # }

            info_integration = IntegrationPasskey(id=self.id, account_id=self.account_id, sign_count=self.sign_count,
                                                  aaguid=self.aaguid, cre_id=self.cre_id,
                                                  public_key_alg=self.public_key_alg, public_key=self.public_key,
                                                  create_on=self.create_on, update_one=self.update_one,
                                                  status=self.status)
            session.add(info_integration)
            session.commit()
            session.close()

            status_create = True
        except Exception as e:
            status_create = False

        return status_create

    async def check_credential(self):
        session = Session()
        info_credential = session.query(IntegrationPasskey).filter(
            IntegrationPasskey.cre_id == self.cre_id,
            IntegrationPasskey.status != self.status).first()
        session.close()

        return info_credential

    async def list_config_integration(self):

        session = Session()
        credentials = session.query(IntegrationPasskey).filter(IntegrationPasskey.account_id == self.account_id,
                                                               IntegrationPasskey.status != self.status).all()

        session.close()
        return credentials


    async def get_all_config(self):
        session = Session()
        credentials = session.query(IntegrationPasskey).filter(
                                                               IntegrationPasskey.status != self.status).all()

        session.close()
        return credentials

    async def get_config_by_id(self, id_config):
        session = Session()
        credentials = session.query(IntegrationPasskey).filter(
            IntegrationPasskey.id == id_config).all()

        session.close()
        return credentials

    async def update_status_config(self, id, status):
        session = Session()
        credentials = update(IntegrationPasskey).where(IntegrationPasskey.id == id,).values(status=status)
        session.commit()
        session.close()

        return credentials

    async def update_number_login(self, account_id, number_sign: int, cre_id):
        session = Session()

        credentials = update(IntegrationPasskey).where(IntegrationPasskey.account_id == account_id,
                                                               IntegrationPasskey.cre_id== cre_id).values(sign_count=number_sign)
        session.execute(credentials)
        session.commit()
        session.close()

        return credentials


    async def get_info_aaguid(self):
        session = Session()
        info_credential = session.query(IntegrationPasskey).filter(
            IntegrationPasskey.aaguid == self.aaguid,
            IntegrationPasskey.account_id == self.account_id,
            IntegrationPasskey.status != "delete").first()
        session.close()

        return info_credential
# session = Session()
# c = session.query(IntegrationPasskey).filter(IntegrationPasskey.account_id == "123123j12nsdha-daskdnas12").all()
#
# print("c")
# Base.metadata.create_all(engine)