from cryptography import x509
from cryptography.hazmat.backends import default_backend

import PyKCS11
import binascii
from datetime import datetime


with open("5_4_result", "rb") as reader:
        data = reader.read()

        print(data)