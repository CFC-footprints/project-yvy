from cloudant import Cloudant
from libs.auth import *

def load_dev_stages():
    client = open_client()
    db_dev = open_db('crop_development_stages', client)
    values = []
    for document in db_dev:
        values.append(document)
    return (values)

def load_crop_coefficients():
    client = open_client()
    db_kc = open_db('crop_coefficients', client)
    values = []
    for document in db_kc:
        values.append(document)
    return (values)

if __name__ == "__main__":
    client = open_client()
    db_dev = open_db('crop_development_stages', client)
    values = []
    for document in db_dev:
        values.append(document)
    print (values)