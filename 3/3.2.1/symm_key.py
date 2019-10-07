import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ALGORITHMS = ['3DES','AES-128','ChaCha20']

def generate_key(file_path, password,algorithm_name):
    password = password.encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend()
    )
    key = kdf.derive(password)
    
    #Now we cut the key down to be usable by a certain algorithm by picking random bytes
    if algorithm_name == "AES-128":
        key = key[:16]
    elif algorithm_name == "3DES":
        key = key[:8]
    elif algorithm_name == "ChaCha20":
        key = key[:64]
    
    with open(file_path,"wb") as writer:
        writer.write(b"Key: " + key)
        writer.write(b"\n")
        writer.write(b"Salt: " + salt)

    return key


def main():
    if len(sys.argv) < 3:
        print("Error! Script must be run like so:")
        print("     $python symm_key.py <file_path> <algorithm>")
        exit(1)

    file_name = sys.argv[1]
    algorithm_name = sys.argv[2]     

    if algorithm_name not in ALGORITHMS:
        print("Error! Invalid algorithm specified")
        print("Allowed algorithms: ")
        print("     3DES     - Triple Data Encryption Standard")
        print("     AES-128  - Advanced Encryption Standard")
        print("     ChaCha20 - Salsa20 variant (ChaCha20)")
        
        exit(1)


    password = input("Insert the password to transform into a key: ")
    
    print(generate_key(file_name,password,algorithm_name))   
    

if __name__ == main():
    main()

