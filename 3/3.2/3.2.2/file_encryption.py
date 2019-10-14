import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ALGORITHMS = ['3DES','AES-128','ChaCha20']

def encrypt_file(file_path, password,algorithm_name):
    password = input("Insert the password to transform into a key: ")



def main():
    if len(sys.argv) < 3:
        print("Error! Script must be run like so:")
        print("     $python file_encryption.py <file_path> <file_path> <algorithm>")
        exit(1)

    target_file_name = sys.argv[1]
    store_file_name = sys.argv[2]
    algorithm_name = sys.argv[3]     

    if algorithm_name not in ALGORITHMS:
        print("Error! Invalid algorithm specified")
        print("Allowed algorithms: ")
        print("     3DES     - Triple Data Encryption Standard")
        print("     AES-128  - Advanced Encryption Standard")
        print("     ChaCha20 - Salsa20 variant (ChaCha20)")
        
        exit(1)

    
    print(encrypt_file(target_file_name,store_file_name,algorithm_name))   
    

if __name__ == main():
    main()

