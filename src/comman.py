from sqlalchemy.orm import declarative_base, sessionmaker
import webauthn
import json

SECRET_KEY = "quang181"
rp_id = "localhost"
rp_name = "Vcc"
# Connet mysql
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:1812001q@123.30.48.240:3307/mydb')

Session = sessionmaker(bind=engine)

rp = webauthn.types.RelyingParty(id="localhost", name="Vcc", icon="VccTest")

MDS_LOCATION = "./fido-mds.json"
with open(MDS_LOCATION, "rb") as r:
    metadata_json = json.load(r)
fido_metadata = webauthn.metadata.FIDOMetadata.from_metadata(metadata_json)