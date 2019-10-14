import sys
import pem
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dsa, rsa, utils, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization, hashes


def rsa_encrypt(message, public_key, storage_file):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(storage_file, "wb") as writer:
        writer.write(ciphertext)


def main():
    if len(sys.argv) < 4:
        print("Error! Script must be run like so:")
        print("     $python rsa_encryption.py <source_file> <file_with_public_key> <storage_file>")
        exit(1)

    target = sys.argv[1]
    key_file = sys.argv[2]
    storage = sys.argv[3]

    with open(key_file, "rb") as reader:
        key = serialization.load_pem_public_key(
            reader.read(),
            backend=default_backend()
        )

    with open(target, "rb") as reader:
        text_to_encrypt = reader.read()

    rsa_encrypt(text_to_encrypt, key, storage)


if __name__ == main():
    main()
