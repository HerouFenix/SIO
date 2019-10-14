import sys
import pem
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dsa, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization

ALLOWED_SIZES = [1024, 2048, 3072, 4096]


def generate_key_pair(public_file, private_file, size):
    # Private Key Generation
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=size,
        backend=default_backend()
    )

    password = input("Insira uma password usada para encriptar a chave privada:")

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            bytes(password, "UTF-8"),
        )
    )

    with open(private_file, "wb") as writer:
        writer.write(pem)
    ######################

    # Public Key Generation
    public_key = private_key.public_key()

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_file, "wb") as writer:
        writer.write(pem)
    ######################


def main():
    if len(sys.argv) < 4:
        print("Error! Script must be run like so:")
        print("     $python key_pair_gen.py <public_key_store_file_path> <private_key_store_file_path> <size>")
        exit(1)

    public_file_name = sys.argv[1]
    private_file_name = sys.argv[2]
    size = int(sys.argv[3])

    if size not in ALLOWED_SIZES:
        print("Error! Invalid algorithm specified")
        print("Allowed algorithms: ")
        print("     1024,2048,3072,4096")

        exit(1)

    generate_key_pair(public_file_name, private_file_name, size)


if __name__ == main():
    main()
