from cryptography import x509
from cryptography.hazmat.backends import default_backend

import PyKCS11
import binascii
from datetime import datetime


def validate_certificate(certificate):
    dates = get_certificate_dates(certificate)

    if datetime.now().timestamp() < dates[0] or datetime.now().timestamp() > dates[1]:
        return False

    return True

def get_certificate_dates(certificate):
    dates = (certificate.not_valid_before.timestamp(),
             certificate.not_valid_after.timestamp())
    return dates


def load_certificate(cert_data):
  
    cert = x509.load_der_x509_certificate(cert_data, default_backend())

    return cert
            

lib = "/usr/local/lib/libpteidpkcs11.so"
pkcs11 = PyKCS11.PyKCS11Lib()
pkcs11.load(lib)

slots = pkcs11.getSlotList()

all_attr = list(PyKCS11.CKA.keys())

#Filter attributes
all_attr = [e for e in all_attr if isinstance(e, int)]

for slot in slots:
    print(pkcs11.getTokenInfo(slot))
    session = pkcs11.openSession(slot)
    for obj in session.findObjects():
        #Get Object attributes
        attr = session.getAttributeValue(obj, all_attr)

        #Create dictionary with attributes
        attr = dict(zip(map(PyKCS11.CKA.get, all_attr), attr))

        print(" Label: ", attr["CKA_LABEL"])

        if attr["CKA_CLASS"] == 1:
            
            cert = load_certificate(bytes(attr["CKA_VALUE"]))
            print("   Issuer: ",cert.issuer.rfc4514_string())
            print("   Subject: ",cert.subject.rfc4514_string(),"\n")
            